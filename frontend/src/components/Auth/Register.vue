<template>
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <div class="text-center">
                <h2>Regístrate</h2>
            </div>
            <ValidationObserver v-slot="{ handleSubmit }">
                <form @submit.prevent="handleSubmit(register)">
                    <div class="form-group">
                        <label for="name">Nombre</label>
                        <ValidationProvider rules="required" v-slot="{ errors }">
                            <input type="text" class="form-control" id="name" v-model="name" maxlength="255">
                            <span class="text-danger">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div class="form-group">
                        <label for="surname">Apellidos</label>
                        <ValidationProvider rules="required" v-slot="{ errors }">
                            <input type="text" class="form-control" id="surname" v-model="surname" maxlength="255">
                            <span class="text-danger">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div class="form-group">
                        <label for="email">Correo</label>
                        <ValidationProvider rules="required" v-slot="{ errors }">
                            <input type="email" class="form-control" id="email" v-model="email" maxlength="255">
                            <span class="text-danger">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div class="form-group">
                        <label for="password">Contraseña</label>
                        <ValidationProvider rules="required|min:5" v-slot="{ errors }">
                            <input type="password" class="form-control" id="password" v-model="password" maxlength="32">
                            <span class="text-danger">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div class="form-group">
                        <label for="current-degree">Titulación que estás cursando</label>
                        <ValidationProvider rules="required" v-slot="{ errors }">
                            <select class="form-control" id="current-degree" v-model="current_degree">
                                <option v-for="(value, key) in degrees" :value="key" :key="key">{{ value }}</option>
                            </select>
                            <span class="text-danger">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div class="form-group">
                        <label for="higher-grade">Curso más alto</label>
                        <ValidationProvider rules="required" v-slot="{ errors }">
                            <select class="form-control" id="higher-grade" v-model="higher_grade">
                                <option value="1">1º</option>
                                <option value="2">2º</option>
                                <option value="3">3º</option>
                                <option value="4">4º</option>
                                <option value="5">5º</option>
                                <option value="6">6º</option>
                            </select>
                            <span class="text-danger">{{ errors[0] }}</span>
                        </ValidationProvider>
                    </div>
                    <div class="form-group">
                        <label for="finished-degrees">Titulación/es acabada/s</label>
                        <select multiple class="form-control" id="finished-degrees" v-model="finished_degrees">
                            <option v-for="(value, key) in degrees" :value="key" :key="key">{{ value }}</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="competences">¿En qué quieres ayudar?</label>
                        <select multiple class="form-control" id="competences" v-model="selected_competences">
                            <option v-for="competence in competences" :value="competence.name" :key="competence.name">
                                {{competence.name}}
                            </option>
                        </select>
                    </div>

                    <!-- <div class="form-group">
                        <div class="custom-file">
                            <input type="file" class="custom-file-input" id="profile-image">
                            <label class="custom-file-label" for="profile-image">Puedes elegir una imagen</label>
                        </div>
                    </div> -->
                    <div class="form-group">
                        <label for="description">Descripción</label>
                        <textarea class="form-control" id="description" v-model="description"></textarea>
                    </div>
                    <div class="text-center">
                        <div class="alert alert-danger" v-if="error">Algo ha fallado. Vuelve a intentarlo</div>
                    </div>
                    <div class="text-center">
                        <button type="submit" class="btn btn-info">Registrarme</button>
                    </div>
                </form>
            </ValidationObserver>
        </div>
    </div>
</template>
<script>
import Vue from 'vue';
import { ValidationObserver, ValidationProvider } from 'vee-validate';
import { min } from '@/validation/validation';
import degrees from '@/data/degrees';

export default {
    name: 'register',
    data() {
        return {
           name: '',
           surname: '',
           email: '',
           password: '',
           degrees,
           current_degree: '',
           higher_grade: '',
           finished_degrees: [],
           competences: [],
           selected_competences: [],
           description: '',
           error: null
        };
    },
    components: {
        ValidationObserver,
        ValidationProvider
    },
    mounted() {
        this.fetchCompetences();
    },
    methods: {
        fetchCompetences() {
            Vue.http.get('competences/')
            .then(response => {
                this.competences = response.body;
            }).catch(error => {
                console.log(error);
            });
        },
        register() {
            Vue.http.post('students/', 
                {
                    user: {
                        first_name: this.name,
                        last_name: this.surname,
                        email: this.email,
                        password: this.password,
                    },
                    degrees: this.buildDegrees(),
                    competences: this.buildCompetences(),
                    description: this.description
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                }
            ).then(response => {
                this.$router.replace({ name: 'login' });
            }).catch(error => {
                this.error = error;
            });
        },
        buildDegrees() {
            let degrees = [];
            let currentDegree = {name: this.current_degree, higher_grade: this.higher_grade, finished: false};
            degrees.push(currentDegree);

            if (this.finished_degrees.length) {
                this.finished_degrees.forEach(degreeName => {
                    let finishedDegree = {name: degreeName, higher_grade: '', finished: true};
                    degrees.push(finishedDegree);
                });
            }
            return degrees;
        },
        buildCompetences() {
            let competences = [];
            this.selected_competences.forEach(competenceName => {
                let competenceObj = {name: competenceName};
                competences.push(competenceObj);
            });
            return competences;
        }
    }
}
</script>