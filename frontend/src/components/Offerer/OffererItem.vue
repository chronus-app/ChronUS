<template>
    <div>
        <button class="btn btn-outline-success">Aceptar</button>
        {{ offerer.full_name }}
    </div>
</template>
<script>

export default {
    props: {
        offerer: {
            type: Object,
            required: true
        }
    },
}
</script>