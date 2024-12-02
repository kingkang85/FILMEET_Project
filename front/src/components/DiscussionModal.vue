<template>
  <Transition name="fade">
    <div v-if="isOpen" class="modal-backdrop" @click.self="closeModal">
      <div class="modal-content">
        <!-- Report Modal -->
        <div v-if="showReportModal" class="report-modal">
          <div class="report-modal-content">
            <h4>채팅 신고하기</h4>
            <form @submit.prevent="submitReport">
              <div class="form-group">
                <label>신고 사유</label>
                <select v-model="reportForm.reason" required>
                  <option value="" disabled selected>신고 사유를 선택해주세요.</option>
                  <option value="spam">스팸</option>
                  <option value="abuse">욕설/비방</option>
                  <option value="adult">음란물</option>
                  <option value="violence">폭력적인 내용</option>
                  <option value="spoiler">스포일러</option>
                  <option value="other">기타</option>
                </select>
              </div>
              <div class="form-group">
                <label>상세 내용</label>
                <textarea 
                  v-model="reportForm.content"
                  placeholder="신고 사유를 자세히 적어주세요."
                  required
                ></textarea>
              </div>
              <div class="report-actions">
                <button type="button" class="btn-secondary" @click="closeReportModal">
                  취소
                </button>
                <button type="submit" class="btn-primary">
                  신고하기
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Original Modal Content -->
        <div class="modal-header">
          <h3>Comments</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>

        <div class="comments-container" ref="commentsContainer">
          <div v-if="isLoading" class="loading-state">
            Loading...
          </div>
          <div v-else-if="sortedDiscussions.myDiscussions.length === 0 && sortedDiscussions.otherDiscussions.length === 0" class="no-comments">
            첫 댓글을 작성해보세요!
          </div>
          <template v-else>
            <div class="discussions-layout">
              <!-- 다른 사람의 댓글 -->
              <div v-for="discussion in sortedDiscussions.otherDiscussions" 
                   :key="discussion.id" 
                   class="comment left-aligned"
                   :class="{ 
                     'comment-hidden': discussion.is_hidden,
                     'comment-hidden-spoiler': discussion.is_hidden && discussion.report_reason === 'spoiler'
                   }">
                <!-- Hidden Comment -->
                <div v-if="discussion.is_hidden && !discussion.showContent" 
                     class="hidden-comment"
                     :class="{ 'spoiler': discussion.report_reason === 'spoiler' }">
                  <p>
                    {{ discussion.report_reason === 'spoiler' 
                        ? '스포일러 신고로 인해 숨겨진 댓글입니다.' 
                        : '신고로 인해 숨겨진 댓글입니다.' }}
                  </p>
                  <button 
                    @click="showHiddenContent(discussion)" 
                    class="show-content-btn"
                    :class="{ 'spoiler': discussion.report_reason === 'spoiler' }"
                  >
                    {{ discussion.report_reason === 'spoiler' ? '스포일러 내용 보기' : '내용 보기' }}
                  </button>
                </div>
                
                <!-- Comment Content -->
                <div v-else>
                  <div class="comment-header">
                    <div class="user-info">
                      <img :src="getImageUrl(discussion.user?.profile_image)" 
                           :alt="discussion.user?.nickname" 
                           class="user-avatar" />
                      <span class="user-nickname">닉네임 : {{ discussion.user?.nickname }}</span>
                      <span class="comment-date">{{ formatDate(discussion.created_at) }}</span>
                    </div>
                    
                    <button 
                      class="action-btn report" 
                      @click="openReportModal(discussion)"
                      :disabled="discussion.is_reported"
                    >
                      {{ discussion.is_reported ? '신고됨' : '신고' }}
                    </button>
                  </div>
                  <p class="comment-content">{{ discussion.content }}</p>
                </div>
              </div>

              <!-- 내 댓글 -->
              <div v-for="discussion in sortedDiscussions.myDiscussions" 
                   :key="discussion.id" 
                   class="comment right-aligned"
                   :class="{ 
                     'comment-hidden': discussion.is_hidden,
                     'comment-hidden-spoiler': discussion.is_hidden && discussion.report_reason === 'spoiler'
                   }">
                <!-- Hidden Comment -->
                <div v-if="discussion.is_hidden && !discussion.showContent" 
                     class="hidden-comment"
                     :class="{ 'spoiler': discussion.report_reason === 'spoiler' }">
                  <p>
                    {{ discussion.report_reason === 'spoiler' 
                        ? '스포일러 신고로 인해 숨겨진 댓글입니다.' 
                        : '신고로 인해 숨겨진 댓글입니다.' }}
                  </p>
                  <button 
                    @click="showHiddenContent(discussion)" 
                    class="show-content-btn"
                    :class="{ 'spoiler': discussion.report_reason === 'spoiler' }"
                  >
                    {{ discussion.report_reason === 'spoiler' ? '스포일러 내용 보기' : '내용 보기' }}
                  </button>
                </div>
                
                <!-- Comment Content -->
                <div v-else>
                  <div class="comment-header">
                    <div class="user-info">
                      <img :src="getImageUrl(discussion.user?.profile_image)" 
                           :alt="discussion.user?.nickname" 
                           class="user-avatar" />
                      <span class="user-nickname">내 댓글</span>
                      <span class="comment-date">{{ formatDate(discussion.created_at) }}</span>
                    </div>
                    
                    <div class="comment-actions">
                      <button class="action-btn" @click="startEdit(discussion)">수정</button>
                      <button class="action-btn delete" @click="deleteComment(discussion.id)">삭제</button>
                    </div>
                  </div>
                  
                  <!-- Edit Mode -->
                  <div v-if="editingId === discussion.id" class="edit-mode">
                    <textarea
                      v-model="editContent"
                      class="edit-textarea"
                      @keyup.enter="updateComment(discussion.id)"
                    ></textarea>
                    <div class="edit-actions">
                      <button class="btn-secondary" @click="cancelEdit">취소</button>
                      <button 
                        class="btn-primary"
                        :disabled="!editContent.trim()"
                        @click="updateComment(discussion.id)"
                      >
                        수정
                      </button>
                    </div>
                  </div>
                  
                  <!-- Normal Mode -->
                  <p v-else class="comment-content">{{ discussion.content }}</p>
                </div>
              </div>
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="pagination">
              <button 
                class="pagination-btn"
                :disabled="currentPage === 1"
                @click="changePage(currentPage - 1)"
              >
                이전
              </button>
              <div class="page-numbers">
                <button 
                  v-for="page in totalPages" 
                  :key="page"
                  class="page-number-btn"
                  :class="{ active: page === currentPage }"
                  @click="changePage(page)"
                >
                  {{ page }}
                </button>
              </div>
              <button 
                class="pagination-btn"
                :disabled="currentPage === totalPages"
                @click="changePage(currentPage + 1)"
              >
                다음
              </button>
            </div>
          </template>
        </div>

        <!-- Comment Input -->
        <div class="comment-input">
          <textarea
            v-model="newComment"
            placeholder="댓글을 입력하세요..."
            @keyup.enter.exact="submitComment"
            @keyup.enter.shift.exact="newComment += '\n'"
          ></textarea>
          <button 
            class="submit-btn"
            :disabled="!newComment.trim() || !user"
            @click="submitComment"
          >
            {{ user ? '작성' : '로그인이 필요합니다' }}
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import { useUserStore } from '@/stores/user'
import { useCommunityStore } from '@/stores/community'
import { storeToRefs } from 'pinia'
import router from '@/router';

const props = defineProps({
 isOpen: Boolean,
 movieId: Number,
})

const emit = defineEmits(['close'])
const userStore = useUserStore()
const communityStore = useCommunityStore()

// Store에서 상태 가져오기 
const { user } = storeToRefs(userStore)
const { discussions, isLoading, error, sortedDiscussions, currentPage, totalPages } = storeToRefs(communityStore)

// 로컬 상태
const newComment = ref('')
const editingId = ref(null)
const editContent = ref('')
const commentsContainer = ref(null)
const showReportModal = ref(false)
const selectedDiscussion = ref(null)
const reportForm = ref({
 reason: '',
 content: ''
})

// 페이지 변경
const changePage = async (page) => {
 try {
   await communityStore.fetchDiscussions(props.movieId, page)
   // 스크롤을 맨 위로
   if (commentsContainer.value) {
     commentsContainer.value.scrollTop = 0
   }
 } catch (error) {
   console.error('Error changing page:', error)
 }
}

// 댓글 불러오기
const fetchDiscussions = async () => {
 try {
   await communityStore.fetchDiscussions(props.movieId, 1) // 첫 페이지부터 시작
   discussions.value = discussions.value.map(d => ({
     ...d,
     showContent: false
   }))
 } catch (error) {
   if (error.response?.status === 401) {
     alert('댓글을 보려면 로그인이 필요합니다.')
     emit('close')
     router.push('/login')
   }
 }
}

// 댓글 작성
const submitComment = async () => {
  if (!newComment.value.trim() || !user.value) return
  
  try {
    await communityStore.createDiscussion(props.movieId, newComment.value)
    newComment.value = ''
    // 새로운 댓글이 추가된 후 첫 페이지로 이동
    await communityStore.fetchDiscussions(props.movieId, 1)
  } catch (error) {
    if (error.response?.status === 401) {
      alert('댓글을 작성하려면 로그인이 필요합니다.')
    }
  }
}
// 댓글 수정 시작
const startEdit = (discussion) => {
 editingId.value = discussion.id
 editContent.value = discussion.content
}

// 댓글 수정 취소
const cancelEdit = () => {
 editingId.value = null
 editContent.value = ''
}

// 댓글 수정
const updateComment = async (discussionId) => {
 if (!editContent.value.trim()) return
 
 try {
   await communityStore.updateDiscussion(discussionId, editContent.value)
   cancelEdit()
   // 현재 페이지 리프레시
   await communityStore.fetchDiscussions(props.movieId, currentPage.value)
 } catch (error) {
   alert('댓글 수정에 실패했습니다.')
 }
}

// 댓글 삭제
const deleteComment = async (discussionId) => {
 if (!confirm('정말로 이 댓글을 삭제하시겠습니까?')) return
 
 try {
   await communityStore.deleteDiscussion(discussionId)
   // 현재 페이지 리프레시
   await communityStore.fetchDiscussions(props.movieId, currentPage.value)
 } catch (error) {
   alert('댓글 삭제에 실패했습니다.')
 }
}

// 신고 모달 열기
const openReportModal = (discussion) => {
 selectedDiscussion.value = discussion
 showReportModal.value = true
}

// 신고 모달 닫기
const closeReportModal = () => {
 showReportModal.value = false
 selectedDiscussion.value = null
 reportForm.value = { reason: '', content: '' }
}

// 신고 제출
const submitReport = async () => {
 if (!selectedDiscussion.value) return
 
 try {
   const reportData = {
     reason: reportForm.value.reason,
     content: reportForm.value.content,  
     discussion: selectedDiscussion.value.id
   }
   
   await communityStore.reportDiscussion(
     selectedDiscussion.value.id,
     reportData
   )
   closeReportModal()
   // 현재 페이지 리프레시
   await communityStore.fetchDiscussions(props.movieId, currentPage.value)
   alert('신고가 접수되었습니다.')
 } catch (error) {
   console.error('Report submission error:', error)
   alert(error.response?.data?.detail || '신고 처리에 실패했습니다.')
 }
}

// 숨겨진 내용 표시
const showHiddenContent = (discussion) => {
 discussion.showContent = true
}

// 날짜 포맷
const formatDate = (dateString) => {
 return new Date(dateString).toLocaleDateString('ko-KR', {
   year: 'numeric',
   month: 'long', 
   day: 'numeric',
   hour: '2-digit',
   minute: '2-digit'
 })
}

// 모달 닫기
const closeModal = () => {
 communityStore.clearDiscussions()
 emit('close')
}

// 현재 사용자의 댓글인지 확인
const isCurrentUser = (userId) => {
 return user.value?.id === userId
}

// 모달이 열릴 때마다 댓글 목록 새로고침
watchEffect(() => {
 if (props.isOpen) {
   fetchDiscussions()
 }
})

const baseURL = 'http://127.0.0.1:8000'

const getImageUrl = (imagePath) => {
  // null이거나 undefined인 경우 기본 이미지 경로 반환
  if (!imagePath) {
    return `${baseURL}/static/images/default_profile.jpg`
  }
  
  // 그 외의 경우 media 경로 추가 (사용자 업로드 이미지)
  return imagePath
}
</script>

<style scoped>
/* Modal Base */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  width: 90%;
  max-width: 800px;
  max-height: 85vh;
  background: #1a1a2e;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(131, 70, 255, 0.1);
}

/* Modal Header */
.modal-header {
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid rgba(131, 70, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(131, 70, 255, 0.05);
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  font-size: 1.5rem;
  color: #fff;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.8rem;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.3s ease;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: rotate(90deg);
}

/* Comments Container */
.comments-container {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1.5rem;
  max-height: 60vh;
}

.comments-container::-webkit-scrollbar {
  width: 8px;
}

.comments-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.comments-container::-webkit-scrollbar-thumb {
  background: rgba(131, 70, 255, 0.3);
  border-radius: 4px;
}

/* Discussion Layout */
.discussions-layout {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

/* Comment Item Styles */
.comment {
  max-width: 85%;
  margin-bottom: 1rem;
  padding: 1.2rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.3s ease;
  word-break: break-all;
}

.comment.left-aligned {
  align-self: flex-start;
  margin-right: auto;
  background: rgba(255, 255, 255, 0.03);
}

.comment.right-aligned {
  align-self: flex-end;
  margin-left: auto;
  background: rgba(131, 70, 255, 0.1);
}

.right-aligned .comment-actions {
  margin-left: auto;
}

.left-aligned .action-btn.report {
  margin-left: auto;
}

/* User Info */
.user-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  flex-wrap: nowrap;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(131, 70, 255, 0.3);
  flex-shrink: 0;
}

.user-nickname {
  font-weight: 500;
  color: #fff;
  font-size: 0.95rem;
}

.comment-date {
  font-size: 0.8rem;
  color: #666;
  margin-right: 0.8rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  flex-wrap: nowrap;
}

/* Comment Actions */
.comment-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.action-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 0.85rem;
  cursor: pointer;
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  transition: color 0.3s ease;
  white-space: nowrap;
}

.action-btn:hover {
  color: #5246ff;
  background: none;
}

.action-btn.delete:hover {
  color: #ff4646;
  background: none;
}

.action-btn.report {
  color: #ff4646;
  background: none;
}

.action-btn.report:disabled {
  color: #666;
  cursor: not-allowed;
}

/* Comment Content */
.comment-content {
  color: #ddd;
  line-height: 1.5;
  white-space: pre-wrap;
  font-size: 0.95rem;
  padding: 0.5rem 0;
}

.no-comments {
  color: #c8c8c8;
}

/* Edit Mode */
.edit-mode {
  margin-top: 0.8rem;
}

.edit-textarea {
  width: 100%;
  min-height: 80px;
  padding: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(131, 70, 255, 0.3);
  border-radius: 8px;
  color: white;
  resize: vertical;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Comment Input */
.comment-input {
  padding: 1.2rem;
  border-top: 1px solid rgba(131, 70, 255, 0.2);
  background: rgba(131, 70, 255, 0.02);
  border-radius: 0 0 16px 16px;
}

.comment-input textarea {
  width: 100%;
  height: 80px;
  padding: 0.8rem;
  margin-bottom: 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(131, 70, 255, 0.2);
  border-radius: 8px;
  color: white;
  resize: none;
  font-size: 0.95rem;
  line-height: 1.5;
}

.comment-input textarea:focus {
  outline: none;
  border-color: #8346ff;
  box-shadow: 0 0 0 2px rgba(131, 70, 255, 0.2);
}

/* Hidden Comment */
.comment-hidden {
  opacity: 0.8;
}

.hidden-comment {
  padding: 1.2rem;
  text-align: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
}

.hidden-comment p {
  color: #ddd;
  margin-bottom: 0.8rem;
  font-size: 0.9rem;
}

.show-content-btn {
  background: none;
  border: 1px solid rgba(131, 70, 255, 0.5);  /* 보라색 테두리 */
  color: #8346ff;  /* 보라색 텍스트 */
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.show-content-btn:hover {
  background: rgba(131, 70, 255, 0.1);  /* 호버 시 살짝 보라색 배경 */
}

.hidden-comment.spoiler {
  background: rgba(255, 193, 7, 0.03);  /* 살짝 노란 배경 */
  border-color: rgba(255, 193, 7, 0.1);
}

.show-content-btn.spoiler {
  border-color: rgba(255, 193, 7, 0.5);  /* 노란색 테두리 */
  color: #ffc107;  /* 노란색 텍스트 */
}

.show-content-btn.spoiler:hover {
  background: rgba(255, 193, 7, 0.1);  /* 호버 시 살짝 노란 배경 */
}


/* Buttons */
.submit-btn,
.btn-primary {
  width: 100%;
  padding: 0.8rem;
  background: #8346ff;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled),
.btn-primary:hover:not(:disabled) {
  background: #9666ff;
}

.submit-btn:disabled,
.btn-primary:disabled {
  background: #444;
  cursor: not-allowed;
  opacity: 0.7;
}

.btn-secondary {
  background: #333;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #444;
}

/* Report Modal */
.report-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #1a1a2e;
  padding: 1.5rem;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  z-index: 1100;
  border: 1px solid rgba(131, 70, 255, 0.2);
}

.report-modal h4 {
  margin-bottom: 1.5rem;
  color: white;
  font-size: 1.2rem;
}

.report-actions {
  display: flex;
  gap: 1rem;  /* 버튼 사이 간격 */
  margin-top: 1.5rem;  /* 위 여백 */
}

.report-actions button {
  flex: 1;  /* 버튼들이 공간을 균등하게 차지 */
  padding: 0.8rem;
  border-radius: 8px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.report-actions .btn-secondary {
  background: #333;
  color: white;
  border: none;
}

.report-actions .btn-secondary:hover {
  background: #444;
}

.report-actions .btn-primary {
  background: #8346ff;
  color: white;
  border: none;
}

.report-actions .btn-primary:hover {
  background: #9666ff;
}

.edit-actions {
 display: flex;
 gap: 1rem;  /* 버튼 사이 간격 */
 margin-top: 1rem;
}

.edit-actions button {
 flex: 1;  /* 버튼들이 공간을 균등하게 차지 */
 padding: 0.8rem;
 border-radius: 8px;
 font-size: 0.95rem;
 cursor: pointer;
 transition: color 0.3s ease;
}

.edit-actions .btn-secondary {
 background: #333;
 color: white;
 border: none;
}

.edit-actions .btn-secondary:hover {
 background: #444;
}

.edit-actions .btn-primary {
 background: #8346ff;
 color: white;
 border: none;
}

.edit-actions .btn-primary:hover {
 background: #9666ff;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #ddd;
}

.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.8rem;
  /* background: #16162a; */
  background: #1d1d35;
  border: 1px solid rgba(131, 70, 255, 0.3);
  border-radius: 8px;
  color: white;
  font-size: 0.95rem;
}

.form-group textarea {
  height: 100px;
  resize: vertical;
}

.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #8346ff;
  box-shadow: 0 0 0 2px rgba(131, 70, 255, 0.2);
}

.form-group textarea::placeholder {
  color: #868686;
}

.form-group select {
  color: #868686;
}

.form-group select:valid {
  color: white;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.8rem;
  padding: 1rem;
  margin-top: 1rem;
  border-top: 1px solid rgba(131, 70, 255, 0.1);
}

.page-numbers {
  display: flex;
  gap: 0.4rem;
}

.page-number-btn {
  min-width: 32px;
  height: 32px;
  padding: 0 0.5rem;
  border: none;
  background: rgba(131, 70, 255, 0.1);
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-number-btn.active {
  background: #8346ff;
}

.page-number-btn:hover:not(.active) {
  background: rgba(131, 70, 255, 0.3);
}

.pagination-btn {
  padding: 0.4rem 1rem;
  background: #8346ff;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.pagination-btn:disabled {
  background: #444;
  cursor: not-allowed;
  opacity: 0.7;
}

.pagination-btn:not(:disabled):hover {
  background: #9666ff;
}

/* Animations */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Responsive */
@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    max-height: 90vh;
  }
  
  .comment {
    max-width: 95%;
  }
  
  .user-info {
    flex-wrap: wrap;
  }

  .comment-date {
    width: 100%;
    margin-top: 0.4rem;
  }
  
  .page-numbers {
    display: none;  /* 모바일에서는 이전/다음만 표시 */
  }
}
</style>