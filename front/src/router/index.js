import { createRouter, createWebHistory } from 'vue-router'
import CoverView from '../views/CoverView.vue'
import HomePageView from '@/views/HomePageView.vue'
import ExploreView from '@/views/ExploreView.vue'
import OttView from '@/views/OttView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import ProfileView from '@/views/ProfileView.vue'
import MovieDetailView from '@/views/MovieDetailView.vue'
import MovieListView from '@/views/MovieListView.vue'
import DirectorDetailView from '@/views/DirectorDetailView.vue'
import ActorDetailView from '@/views/ActorDetailView.vue'
import FavoriteMoviesView from '@/views/FavoriteMoviesView.vue'
import FavoriteActorsView from '@/views/FavoriteActorsView.vue'
import FavoriteDirectorsView from '@/views/FavoriteDirectorsView.vue'
import WorldcupView from '@/views/WorldcupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'cover',
      component: CoverView,
    },
    {
      path: '/main',
      name: 'main',
      component: HomePageView,
    },
    {
      // path: '/movies?search={keyword}',
      path: '/movies/search',
      name: 'search',
      component: ExploreView,
    },
    {
      // path: '/recommendations/ott/:id',
      path: '/recommendations/ott',
      name: 'ott',
      component: OttView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/movies/',
      name: 'movielist',
      component: MovieListView,
    },
    {
      path: '/movies/:id',  // :id로 변경
      name: 'moviedetail',
      component: MovieDetailView,
      props: true  // route.params를 props로 전달
    },
    {
      path: '/director/:id',
      name: 'directordetail',
      component: DirectorDetailView,
    },
    {
      path: '/actor/:id',
      name: 'actordetail',
      component: ActorDetailView,
    },
    {
      // path: '/actors/:id',
      path: '/wishlist/movies',
      name: 'wishmovies',
      component: FavoriteMoviesView,
    },
    {
      // path: '/actors/:id',
      path: '/wishlist/actors',
      name: 'wishactors',
      component: FavoriteActorsView,
    },
    {
      // path: '/actors/:id',
      path: '/wishlist/directors',
      name: 'wishdirectors',
      component: FavoriteDirectorsView,
    },
    {
      path: '/worldcup/',
      name: 'worldcup',
      component: WorldcupView
    }
  ],
})

export default router
