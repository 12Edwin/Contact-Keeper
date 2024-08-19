<template>
    <div>

    </div>
</template>

<script>
    export default {
        name: "UpdateEventModal",
        props: {
            event: {
                type: Object,
                required: true
            }
        },
        data(){
            return {
                types: [
                    { label: 'Reunión', value: 'meeting' },
                    { label: 'Sesión', value: 'session' },
                    {label: 'Cumpleaños', value: 'birthday'},
                    {label: 'Otro', value: 'other'}
                ],
                invites: [],
                groups: [],
            }
        }
    }
</script>

<style lang="scss" scoped>

</style>