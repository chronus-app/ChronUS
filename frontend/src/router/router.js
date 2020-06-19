import Vue from 'vue';
import VueRouter from 'vue-router';

import Register from '@/components/Auth/Register';
import Login from '@/components/Auth/Login';
import Landing from '@/components/Landing';
import Home from '@/components/Home';
import CollaborationRequestCreation from '@/components/CollaborationRequest/CollaborationRequestCreation';
import CollaborationRequestList from '@/components/CollaborationRequest/CollaborationRequestList';
import CollaborationRequestDetails from '@/components/CollaborationRequest/CollaborationRequestDetails';
import CollaborationDetails from '@/components/Collaboration/CollaborationDetails';

import store from '@/store/store';

Vue.use(VueRouter);

const router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path: "/register",
            name: "register",
            component: Register,
            meta: { requiresVisitor: true, title: "Regístrate" },
        },
        {
            path: "/login",
            name: "login",
            component: Login,
            meta: { requiresVisitor: true, title: "Accede" },
        },
        {
            path: "/",
            name: "landing",
            component: Landing,
            meta: { requiresVisitor: true, title: "Chronus" },
        },
        {
            path: "/home",
            name: "home",
            component: Home,
            meta: { requiresAuth: true, title: "Inicio" },
        },
        {
            path: "/collaboration-requests/create",
            name: "collaboration-request-creation",
            component: CollaborationRequestCreation,
            meta: { requiresAuth: true, title: "Creación de solicitud de colaboración" },
        },
        {
            path: "/collaboration-requests",
            name: "collaboration-request-list",
            component: CollaborationRequestList,
            meta: { requiresAuth: true, title: "Solicitudes de colaboración" },
        },
        {
            path: "/collaboration-requests/:id",
            name: "collaboration-request-details",
            component: CollaborationRequestDetails,
            meta: { requiresAuth: true, title: "Detalle de solicitud de colaboración" },
        },
        {
            path: "/collaborations/:id",
            name: "collaboration-details",
            component: CollaborationDetails,
            meta: { requiresAuth: true, title: "Detalle de colaboración" },
        },
    ]
});

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!store.getters.loggedIn) {
        next({
          name: 'login',
        })
      } else {
        next()
      }
    } else if (to.matched.some(record => record.meta.requiresVisitor)){
        if (store.getters.loggedIn) {
            next({
                name: 'home',
            })
        } else {
            next()
        }
    } else {
        next()
    }
  });

export default router;
