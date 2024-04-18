import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/subject',
      name: 'subject',
      component: () => import('../views/subjectView.vue')
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../views/tetsView.vue')
    },
    // {
    //   path: '/login',
    //   name: 'login',
    //   component: () => import('../views/loginView.vue')
    // },
    {
      path: '/createExam',
      name: 'createExam',
      component: () => import('../views/CreateExamView.vue')
    },
    {
      path: '/importAnswer',
      name: 'importAnswer',
      component: () => import('../views/ImportAnswerView.vue')
    },
    {
      path: '/UploadExam',
      name: 'UploadExam',
      component: () => import('../views/UploadAnswerStudentView.vue')
    },
    {
      path: '/CheckAnswer',
      name: 'CheckAnswer',
      component: () => import('../views/CheckAnswerView.vue')
    },
    {
      path: '/InsertStudent',
      name: 'InsertStudent',
      component: () => import('../views/InsertStudentView.vue')
    },
    {
      path: '/ListOfStu',
      name: 'ListOfStu',
      component: () => import('../views/ListOfStudent.vue')
    },
    {
      path: '/DetailOverall/:id_exam',
      name: 'DetailOverall',
      component: () => import('../views/DetailOverall.vue')
    },
    {
      path: '/hExam/:code_subject',
      name: 'hExam',
      component: () => import('../views/HomeExam.vue')
    },
    // {
    //   path: '/register',
    //   name: 'register',
    //   component: () => import('../views/RegisterView.vue')
    // },
    {
      path: '/student-answer/:id_exam/:id_student',
      name: 'StudentAnswer',
      component: () => import('../views/StudentAnswer.vue')
    },
    {
      path: '/EditSubject/:code_subject',
      name: 'EditSubject',
      component: () => import('../views/EditSubject.vue')
    },
    {
      path: '/EditExam/:id_exam',
      name: 'EditExam',
      component: () => import('../views/EditExam.vue')
    },
    {
      path: '/Profile',
      name: 'Profile',
      component: () => import('../views/ProfileView.vue')
    },
    {
      path: '/loginAdmin',
      name: 'admin',
      component: () => import('../views/loginAdmin.vue')
    },
    {
      path: '/addAdmin',
      name: 'addAdmin',
      component: () => import('../views/addAdmin.vue')
    },
    {
      path: '/manageUser',
      name: 'manageUser',
      component: () => import('../views/manageUser.vue')
    },
  ]
})

export default router
