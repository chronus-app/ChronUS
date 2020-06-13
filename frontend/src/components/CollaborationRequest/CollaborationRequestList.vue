<template>
    <div class="container pt-5">
        <div class="row">
            <div 
                v-for="collaboration_request in collaboration_requests"
                :key="collaboration_request.id"
                class="col-md-4"
            >
                <CollaborationRequestItem :collaboration_request="collaboration_request"></CollaborationRequestItem>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue';
import CollaborationRequestItem from '@/components/CollaborationRequest/CollaborationRequestItem';

export default {
    name: 'collaboration-request-list',
    data() {
        return {
            collaboration_requests: []
        };
    },
    components: {
        CollaborationRequestItem
    },
    mounted() {
        this.fetchCollaborationRequests();
    },
    methods: {
        fetchCollaborationRequests() {
            Vue.http.get('collaboration-requests/',
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${this.$store.state.auth.token}`
                    }
                }
            )
            .then(response => {
                this.collaboration_requests = response.body;
            }).catch(error => {
                console.log(error);
            });
        },
    }
}
</script>