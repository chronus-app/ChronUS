<template>
    <div class="container pt-5">
        <div class="row" v-if="collaboration.title">
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
            <div class="content col-md-7">
                <div id ="messages" class="messages">
                    <ul>
                        <li v-for="message in messages" :key="message.id" :class="{ replies: logged_student.user && logged_student.user.id == message.sender, sent: logged_student.user && !(logged_student.user.id == message.sender) }">
                            <p>{{ message.text }}</p>
                        </li>
                    </ul>
                </div>
                <div class="message-input">
                    <div class="wrap">
                        <input id="chat-message-input" type="text" placeholder="Escribe tu mensaje aquí..." @keyup.enter="clickSend()"/>
                        <button id="chat-message-submit" class="btn btn-outline-secondary" @click="sendMessage()">Enviar</button>
                    </div>
                </div>
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
            messages: [],
            chatSocket: {}
        }
    },
    mounted() {
        
        this.fetchCollaboration();
        this.$store.dispatch('retrieveLoggedStudent')
        .then(response => {
            this.logged_student = response.body;
            this.fetchMessages()
            this.openSocketConnection();
            let vm = this;
            this.chatSocket.onmessage = function(event) {
                let messageString = event.data.split('\'').join('"');
                let messageObject = JSON.parse(messageString);
                vm.messages.push(messageObject);
            }
        }).catch(error => {
            console.log(error);
        });
    },
    updated() {
        var messagesDiv = document.getElementById("messages");
        messagesDiv.scrollTop = messagesDiv.scrollHeight - messagesDiv.clientHeight;
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
                this.$router.replace({ name: '404' });
            });
        },
        fetchMessages() {
            Vue.http.get(`messages/?collaboration_id=${this.$route.params.id}`,
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${this.$store.state.auth.token}`
                    }
                }
            )
            .then(response => {
                this.messages = response.body;
            }).catch(error => {
                console.log(error);
            });
        },
        openSocketConnection() {
            this.chatSocket = new WebSocket(
                'ws://127.0.0.1:8000'
                + '/ws/collaborations/'
                + this.$route.params.id
                + '/?token='
                + this.$store.state.auth.token
            );
        },
        collaborationImage() {
            let competences = this.collaboration.competences;
            let imagePath = '';
            if (!competences.length) {
                imagePath =  require('@/assets/colors.png');
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
        clickSend() {
            document.querySelector('#chat-message-submit').click();
        },
        sendMessage() {
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            this.chatSocket.send(message);
            messageInputDom.value = '';
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
    },
}
</script>
<style scoped>
    .card {
        border: none;
    }
    .content .messages {
        height: 500px;
        min-height: calc(100% - 93px);
        max-height: calc(100% - 93px);
        overflow-y: scroll;
        overflow-x: hidden;
    }
    .content .messages::-webkit-scrollbar {
        width: 8px;
        background: transparent;
    }
    .content .messages::-webkit-scrollbar-thumb {
        background-color: rgba(0, 0, 0, 0.3);
    }
    .content .messages ul li {
        display: inline-block;
        clear: both;
        float: left;
        margin: 15px 15px 5px 15px;
        width: calc(100% - 25px);
        font-size: 0.9em;
    }
    .content .messages ul li:nth-last-child(1) {
        margin-bottom: 20px;
    }
    .content .messages ul li.sent img {
    margin: 6px 8px 0 0;
    }
    .content .messages ul li.sent p {
    background: #435f7a;
    color: #f5f5f5;
    }
    .content .messages ul li.replies img {
    float: right;
    margin: 6px 0 0 8px;
    }
    .content .messages ul li.replies p {
    background: #f5f5f5;
    float: right;
    }
    .content .messages ul li img {
    width: 22px;
    border-radius: 50%;
    float: left;
    }
    .content .messages ul li p {
    display: inline-block;
    padding: 10px 15px;
    border-radius: 20px;
    max-width: 205px;
    line-height: 130%;
    }
    .content .message-input {
    position: absolute;
    bottom: 0;
    width: 100%;
    z-index: 99;
    }
    .content .message-input .wrap {
    position: relative;
    }
    .content .message-input .wrap input {
    font-family: "proxima-nova",  "Source Sans Pro", sans-serif;
    float: left;
    border: none;
    width: calc(100% - 90px);
    padding: 11px 32px 10px 8px;
    font-size: 0.8em;
    color: #32465a;
    }
    .content .message-input .wrap input:focus {
    outline: none;
    }
    .content .message-input .wrap .attachment {
    position: absolute;
    right: 60px;
    z-index: 4;
    margin-top: 10px;
    font-size: 1.1em;
    color: #435f7a;
    opacity: .5;
    cursor: pointer;
    }
    .content .message-input .wrap .attachment:hover {
    opacity: 1;
    }
    .content .message-input .wrap button {
    float: right;
    border: none;
    width: 50px;
    padding: 12px 0;
    cursor: pointer;
    background: #32465a;
    color: #f5f5f5;
    }
    .content .message-input .wrap button:hover {
    background: #435f7a;
    }
    .content .message-input .wrap button:focus {
    outline: none;
    }
</style>