<template>
    <div class="container pt-5">
        <div class="row">
            <div class="card col-md-7">
                <img v-if="collaboration_request.competences" style="height: 300px;" class="card-img-top" :src="collaborationRequestImage()" :alt="collaboration_request.title">
                <div class="card-body pl-0">
                    <h4 class="card-title">{{ collaboration_request.title }}</h4>
                    <p class="card-text">{{ collaboration_request.description }}</p>
                </div>
            </div>
            <div class="col-md-4">
                <h5>Publicada por:</h5>
                <div v-if="collaboration_request.applicant">{{ collaboration_request.applicant.full_name }}</div>
                <div class="mt-5">
                    <div v-if="collaboration_request.deadline"><h6>Fecha límite: </h6><span>{{ formattedDate }}</span></div>
                    <div class ="mt-2" v-if="collaboration_request.requested_time"><h6>Tiempo solicitado: </h6><span>{{ requestedTime }}</span></div>
                </div>
                <button v-if="collaboration_request.applicant
                                && collaboration_request.offerers
                                && logged_student.user 
                                && (collaboration_request.applicant.id != logged_student.user.id)
                                && !getOffererIds().includes(logged_student.user.id)" 
                        class="btn btn-outline-info mt-5"
                >
                    Ofrecer colaboración
                </button>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue';

export default {
    name: 'collaboration-request-details',
    data() {
        return {
            collaboration_request: {},
            logged_student: {}
        }
    },
    props: {
        id: {
            type: Number|String,
            required: true
        }
    },
    mounted() {
        this.fetchCollaborationRequest();
        this.$store.dispatch('retrieveLoggedStudent')
        .then(response => {
           this.logged_student = response.body;
        }).catch(error => {
            console.log(error);
        })
    },
    methods: {
        fetchCollaborationRequest() {
            Vue.http.get(`collaboration-requests/${this.id}`,
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${this.$store.state.auth.token}`
                    }
                }
            )
            .then(response => {
                this.collaboration_request = response.body;
            }).catch(error => {
                console.log(error);
            });
        },
        collaborationRequestImage() {
            let competences = this.collaboration_request.competences;
            let imagePath = '';
            if (!competences.length) {
                imagePath =  require('@/assets/i_dont_know.jpg');
            } else if (competences.length > 1) {
                imagePath = require('@/assets/colors.png');
            } else if (competences[0].name == 'Actividad física') {
                imagePath = require('@/assets/physical_activity.png');
            } else if (competences[0].name == 'Matemáticas') {
                imagePath = require('@/assets/mathematics.jpg');
            } else if (competences[0].name == 'Ciencias sociales') {
                imagePath = require('@/assets/social_sciences.jpg');
            } else if (competences[0].name == 'Audiovisual') {
                imagePath = require('@/assets/audiovisual.jpg');
            } else if (competences[0].name == 'Idiomas') {
                imagePath = require('@/assets/languages.png');
            } else if (competences[0].name == 'Informática') {
                imagePath = require('@/assets/computing.jpg');
            } else if (competences[0].name == 'Ciencia') {
                imagePath = require('@/assets/science.png');
            }
            return imagePath;
        },
        convertMinutesToString(minutes) {
            let minutesString = '';
            switch(minutes) {
                case '25':
                    minutesString = '15 minutos';
                    break;
                case '50':
                    minutesString = '30 minutos';
                    break;
                case '75':
                    minutesString = '45 minutos';
                    break;
            }
            return minutesString;
        },
        getOffererIds() {
            let offerers = this.collaboration_request.offerers;
            let offererIds = [];
            offerers.forEach(offerer => {
                offererIds.push(offerer.id);
            })
            return offererIds;
        }
    },
    computed: {
        formattedDate() {
            let deadline = new Date(this.collaboration_request.deadline);
            let day = deadline.getDate();
            let month = deadline.getMonth() + 1;
            let year = deadline.getFullYear();
            return `${day}/${month}/${year}`
        },
        requestedTime() {
            let requestedTime = this.collaboration_request.requested_time;
            let splitRequestedTime = requestedTime.split('.');
            let requestedTimeString = '';
            if (splitRequestedTime[0] == '0') {
                requestedTimeString = this.convertMinutesToString(splitRequestedTime[1]);
            } else {
                requestedTimeString = splitRequestedTime[0];
                requestedTimeString += splitRequestedTime[0] == '1' ? ' hora' : ' horas';
                if (splitRequestedTime[1] != '00') {
                    requestedTimeString += ' y ' + this.convertMinutesToString(splitRequestedTime[1]);
                }
            }
            return requestedTimeString;
        },
    }
}
</script>
<style scoped>
    .card {
        border: none;
    }
</style>