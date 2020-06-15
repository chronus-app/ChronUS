<template>
    <div class="container pt-5">
        <div class="row">
            <div class="card col-md-5">
                <img  v-if="collaboration.competences" style="height: 300px;" class="card-img-top" :src="collaborationImage()" :alt="collaboration.title">
                <div class="card-body pl-0">
                    <h4 class="card-title">{{ collaboration.title }}</h4>
                    <p class="card-text">{{ collaboration.description }}</p>
                </div>
                <div v-if="loggedIsApplicant">
                    <h5>Colabora contigo:</h5>
                    <div>{{ collaboration.collaborator.full_name }}</div>
                </div>
                <div v-if="loggedIsCollaborator" >
                    <h5>Colaboras con:</h5>
                    <div>{{ collaboration.applicant.full_name }}</div>
                </div>
                 <div class="mt-3">
                    <div v-if="collaboration.deadline"><h6>Fecha límite: </h6><span>{{ formattedDate }}</span></div>
                    <div class ="mt-2" v-if="collaboration.requested_time"><h6>Tiempo solicitado: </h6><span>{{ requestedTime }}</span></div>
                </div>
            </div>
            <div class="col-md-7">
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue';

export default {
    name: 'collaboration-details',
    data() {
        return {
            collaboration: {},
            logged_student: {},
        }
    },
    mounted() {
        this.fetchCollaboration();
        this.$store.dispatch('retrieveLoggedStudent')
        .then(response => {
           this.logged_student = response.body;
        }).catch(error => {
            console.log(error);
        })
    },
    methods: {
        fetchCollaboration() {
            Vue.http.get(`collaborations/${this.$route.params.id}`,
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${this.$store.state.auth.token}`
                    }
                }
            )
            .then(response => {
                this.collaboration = response.body;
            }).catch(error => {
                console.log(error);
            });
        },
        collaborationImage() {
            let competences = this.collaboration.competences;
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
    },
    computed: {
        formattedDate() {
            let deadline = new Date(this.collaboration.deadline);
            let day = deadline.getDate();
            let month = deadline.getMonth() + 1;
            let year = deadline.getFullYear();
            return `${day}/${month}/${year}`
        },
        requestedTime() {
            let requestedTime = this.collaboration.requested_time;
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
        loggedIsApplicant() {
            return this.logged_student.user 
                    && this.collaboration.collaborator 
                    && (this.logged_student.user.id == this.collaboration.applicant.id);
        },
        loggedIsCollaborator() {
            return this.logged_student.user 
                    && this.collaboration.applicant 
                    && (this.logged_student.user.id == this.collaboration.collaborator.id);
        },
    }
}
</script>
<style scoped>
    .card {
        border: none;
    }
</style>