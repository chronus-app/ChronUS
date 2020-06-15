<template>
    <div>
        <h5>Ofrecimientos de colaboración:</h5>
        <div class="row">
            <div v-for="offerer in offerers"
                :key="offerer.id"
                class="col-4 mb-4 mt-2"
            >
                <OffererItem :offerer="offerer" :collaboration_request_id="collaboration_request_id"></OffererItem>
            </div>
        </div>
    </div>
</template>
<script>
import OffererItem from '@/components/Offerer/OffererItem';

export default {
    props: {
        offerers: {
            type: Array,
            required: true
        },
        collaboration_request_id: {
            type: Number,
            required: true
        }
    },
    components: {
        OffererItem
    }
    
}
</script>