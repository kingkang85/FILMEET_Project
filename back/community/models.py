from django.db import models

# Create your models here.
class Discussion(models.Model):
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)
    report_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']  # 최신 댓글이 먼저 표시되도록

    def __str__(self):
        return f"{self.user.username}'s comment on {self.movie.title}"
    

class Report(models.Model):
    REPORT_REASONS = [
        ('spam', '스팸'),
        ('abuse', '욕설/비방'),
        ('adult', '음란물'),
        ('violence', '폭력적인 내용'),
        ('spoiler', '스포일러'),
        ('other', '기타'),
    ]

    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reported_discussions')
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 한 사용자가 같은 댓글을 중복 신고할 수 없도록
        unique_together = ('discussion', 'reporter')