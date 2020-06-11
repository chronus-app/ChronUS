<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="d-flex flex-grow-1">
            <div class="w-100 text-right">
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#myNavbar7">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
        </div>
        <div class="collapse navbar-collapse flex-grow-1 text-right" id="myNavbar7">
            <ul class="navbar-nav ml-auto flex-nowrap">
                <li v-if="!loggedIn" class="nav-item">
                    <router-link :to="{ name: 'login' }" class="nav-link">Iniciar sesión</router-link>
                </li>
                <li v-if="!loggedIn" class="nav-item">
                    <router-link :to="{ name: 'register' }" class="nav-link">Registrarse</router-link>
                </li>
                <li v-else class="nav-item"><button @click="logout()" class="btn btn-outline-danger my-2 my-sm-0">Cerrar sesión</button></li>
            </ul>
        </div>
    </nav>
</template>
<script>
export default {
    name: 'navbar',
    methods: {
        logout() {
            this.$store.dispatch('destroyToken')
            .then(response => {
                this.$router.replace({ name: 'landing' });
            })
        }
    },
    computed: {
        loggedIn() {
            return this.$store.getters.loggedIn;
        }
    }
}
</script>