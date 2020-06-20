<template>
    <div v-if="logged_student.available_time" class="container">
        <div class="row">
            <div class="col-md-6 offset-md-3 text-center mt-5">
                <h3>Bienvenid@ a Chronus, la red colaborativa de la Universidad de Sevilla</h3>
                <h4 class="mt-5">Tiempo disponible:</h4>
                <h5>{{ availableTime }}</h5>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'home',
    data() {
        return {
            logged_student: {}
        }
    },
    mounted() {
        this.$store.dispatch('retrieveLoggedStudent')
        .then(response => {
            this.logged_student = response.body;
        }).catch(error => {
            console.log(error);
        });
    },
    methods: {
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
                default:
                    minutesString = 'No tienes tiempo disponible'
            }
            return minutesString;
        },
    },
    computed: {
        availableTime() {
            let availableTime = this.logged_student.available_time;
            let splitAvailableTime = availableTime.split('.');
            let availableTimeString = '';
            if (splitAvailableTime[0] == '0') {
                availableTimeString = this.convertMinutesToString(splitAvailableTime[1]);
            } else {
                availableTimeString = splitAvailableTime[0];
                availableTimeString += splitAvailableTime[0] == '1' ? ' hora' : ' horas';
                if (splitAvailableTime[1] != '00') {
                    availableTimeString += ' y ' + this.convertMinutesToString(splitAvailableTime[1]);
                }
            }
            return availableTimeString;
        },
    }
}
</script>