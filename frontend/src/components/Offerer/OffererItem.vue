<template>
    <div>
        <button @click="createCollaboration()" class="btn btn-outline-success">Aceptar</button>
        {{ offerer.full_name }}
    </div>
</template>
<script>
import Vue from 'vue';

export default {
    name: 'offerer-item',
    props: {
        offerer: {
            type: Object,
            required: true
        },
        collaboration_request_id: {
            type: Number,
            required: true
        }
    },
    methods: {
        createCollaboration() {
            Vue.http.post('collaborations/',
                {
                    collaborator: this.offerer.id,
                    collaboration_request: this.collaboration_request_id
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${this.$store.state.auth.token}`
                    }
                }
            )
            .then(response => {
               this.$router.replace({ name: 'collaboration-details', params: { id: response.body.id } }); 
            }).catch(error => {
                console.log(error);
            });
        }
    }
}
</script>