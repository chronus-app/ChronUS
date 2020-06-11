import Vue from 'vue';
import VueRouter from 'vue-router';

import Register from '@/components/Auth/Register';
import Login from '@/components/Auth/Login';
import Home from '@/components/Home';

import store from '@/store/store';

Vue.use(VueRouter);

const router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path: "/register",
            name: "register",
            component: Register,
            meta: { Auth: false, title: "Regístrate" },
        },
        {
            path: "/login",
            name: "login",
            component: Login,
            meta: { Auth: false, title: "Accede" },
            beforeEnter: (to, from, next) => {
                if (store.getters.loggedIn) {
                    next({ name: 'home' });
                } else {
                    next();
                }
            }
        },
        {
            path: "/home",
            name: "home",
            component: Home,
            meta: { Auth: true, title: "Chronus" },
            beforeEnter: (to, from, next) => {
                if (!store.getters.loggedIn) {
                    next({ name: 'login' });
                } else {
                    next();
                }
            }
        },
    ]
});

export default router;
