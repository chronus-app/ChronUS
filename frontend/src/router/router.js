import Vue from 'vue'
import VueRouter from 'vue-router'

import Register from '@/components/Auth/Register'

Vue.use(VueRouter)

const router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path: "/register",
            name: "register",
            component: Register,
            meta: { Auth: false, title: "Regístrate" },
        },
    ]
})

export default router
