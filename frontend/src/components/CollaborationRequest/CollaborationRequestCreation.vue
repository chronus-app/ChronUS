<template>
    <div class="col-md-4 offset-md-4">
        <div class="text-center">
            <h2>Crea una solicitud de colaboración</h2>
        </div>
        <ValidationObserver v-slot="{ handleSubmit }">
            <form @submit.prevent="handleSubmit(createCollaborationRequest)">
                <div class="form-group">
                    <label for="title">Título</label>
                    <ValidationProvider rules="required" v-slot="{ errors }">
                        <input type="text" class="form-control" id="title" v-model="title" maxlength="100">
                        <span class="text-danger">{{ errors[0] }}</span>
                    </ValidationProvider>
                </div>
                <div class="form-group">
                    <label for="description">Descripción</label>
                    <textarea class="form-control" id="description" v-model="description"></textarea>
                </div>
                <div class="form-group">
                    <label for="deadline">Fecha límite</label>
                    <ValidationProvider rules="required|date_gte" v-slot="{ errors }">
                        <input type="date" class="form-control" id="deadline" v-model="deadline">
                        <span class="text-danger">{{ errors[0] }}</span>
                    </ValidationProvider>
                </div>
                <div class="form-group">
                    <label for="requested-time">Tiempo solicitado</label>
                    <ValidationProvider rules="required|min_time|val_minutes" v-slot="{ errors }">
                        <input type="text" pattern="[0-9]+:[0-9]+" placeholder="hh:mm" class="form-control" id="requested-time" v-model="requested_time">
                        <span class="text-danger">{{ errors[0] }}</span>
                    </ValidationProvider>
                </div>
                <div class="form-group">
                    <label for="competences">¿En qué quieres ayudar?</label>
                    <select multiple class="form-control" id="competences" v-model="selected_competences">
                        <option v-for="competence in competences" :value="competence.name" :key="competence.name">
                            {{competence.name}}
                        </option>
                    </select>
                </div>
                <div class="text-center mb-2">
                    <span v-if="error" class="text-danger">{{ error }}</span>
                </div>
                <div class="text-center">
                    <button type="submit" class="btn btn-info">Publicar</button>
                </div>
            </form>
        </ValidationObserver>
    </div>
</template>
<script>
import Vue from 'vue';
import { ValidationObserver, ValidationProvider } from 'vee-validate';
import { date_gte, min_time, val_minutes } from '@/validation/validation';

export default {
    name: 'collaboration-request-creation',
    data() {
        return {
            title: '',
            description: '',
            deadline: '',
            requested_time: '',
            competences: [],
            selected_competences: [],
            error: ''
        }
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
        createCollaborationRequest() {
            Vue.http.post('collaboration-requests/', 
                {
                    title: this.title,
                    description: this.description,
                    deadline: this.formattedDate,
                    requested_time: this.requestedTime,
                    competences: this.buildCompetences()
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${this.$store.state.auth.token}`
                    }
                }
            ).then(response => {
                this.$router.replace({ name: 'my-collaboration-request-list' });
            }).catch(error => {
                this.error = error.body.non_field_errors[0];
            });
        },
        buildCompetences() {
            let competences = [];
            this.selected_competences.forEach(competenceName => {
                let competenceObj = {name: competenceName};
                competences.push(competenceObj);
            });
            return competences;
        },
        convertMinutesToDecimal(minutes) {
            let minutesString = '';
            switch(minutes) {
                case '15':
                    minutesString = '25';
                    break;
                case '30':
                    minutesString = '50';
                    break;
                case '45':
                    minutesString = '75';
                    break;
                default:
                    minutesString = '0';
            }
            return minutesString;
        },
    },
    computed: {
        formattedDate() {
            let deadline = new Date(this.deadline);
            let day = deadline.getDate();
            let month = deadline.getMonth() + 1;
            let year = deadline.getFullYear();
            return `${year}-${month}-${day}`;
        },
        requestedTime() {
            let requestedTime = this.requested_time;
            let splittedTime = requestedTime.split(':');
            let wholePart = splittedTime[0];
            let decimalPart = this.convertMinutesToDecimal(splittedTime[1]);
            return `${wholePart}.${decimalPart}`;
        }
    }
}
</script>