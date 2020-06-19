<template>
    <div class="container pt-5">
        <div class="row">
            <div 
                v-for="collaboration in collaborations"
                :key="collaboration.id"
                class="col-md-4 mb-4"
            >
                <CollaborationItem :collaboration="collaboration"></CollaborationItem>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue';
import CollaborationItem from '@/components/Collaboration/CollaborationItem';

export default {
    name: 'collaboration-list',
    data() {
        return {
            collaborations: []
        };
    },
    components: {
        CollaborationItem
    },
    mounted() {
        this.fetchCollaborations();
    },
    methods: {
        fetchCollaborations() {
            Vue.http.get('collaborations/',
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${this.$store.state.auth.token}`
                    }
                }
            )
            .then(response => {
                this.collaborations = response.body;
            }).catch(error => {
                console.log(error);
            });
        },
    }
}
</script>