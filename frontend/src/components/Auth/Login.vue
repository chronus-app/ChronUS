<template>
    <div class="row">
        <div class="col-md-4 offset-md-4">
            <div class="text-center">
                <h2>Inicia sesión</h2>
            </div>
            <ValidationObserver v-slot="{ handleSubmit }">
                <form @submit.prevent="handleSubmit(login)">
                    <div class="form-group">
                        <label for="email">Correo</label>
                        <ValidationProvider rules="required" v-slot="{ errors }">
                            <input type="email" class="form-control" id="email" v-model="email" maxlength="255">
                            <span class="text-danger">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div class="form-group">
                        <label for="password">Contraseña</label>
                        <ValidationProvider rules="required" v-slot="{ errors }">
                            <input type="password" class="form-control" id="password" v-model="password" maxlength="32">
                            <span class="text-danger">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div class="text-center">
                        <div class="alert alert-danger" v-if="error">Credenciales incorrectos. Vuelve a intentarlo</div>
                    </div>
                    <div class="text-center">
                        <button type="submit" class="btn btn-info">Iniciar sesión</button>
                    </div>
                </form>
            </ValidationObserver>
        </div>
    </div>
</template>
<script>
import Vue from 'vue';
import { ValidationObserver, ValidationProvider } from 'vee-validate';

export default {
    name: 'login',
    data() {
        return {
            email: '',
            password: '',
            error: null
        };
    },
    components: {
        ValidationObserver,
        ValidationProvider
    },
    methods: {
        login() {
            this.$store.dispatch('retrieveToken', {
                email: this.email,
                password: this.password
            }).then(response => {
                this.$router.replace({ name: 'home' });
            }).catch(error => {
                this.error = error;
            });
        }
    }
}
</script>