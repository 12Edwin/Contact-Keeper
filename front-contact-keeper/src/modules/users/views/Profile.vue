<template>
    <div class="main-content">
        <div class="content">
            <Panel header="Perfil" class="shadow-lg">
                <div class="avatar">{{ getAvatarLetter() }}</div>
                <div class="user-info">
                    <h2>Nombre: {{ getName() }}</h2>
                    <h2>Correo: {{ getEmail() }}</h2>
                </div>
            </Panel>
        </div>
    </div>
</template>

<script>
import Panel from 'primevue/panel/Panel';
import utils from '@/kernel/utils';

export default {
    name: 'Profile',
    components: {
        Panel
    },
    methods: {
        getEmail() {
            return utils.getEmailFromToke();
        },
        getName() {
            return utils.getUserFromToke();
        },
        getAvatarLetter() {
            return utils.getUserFromToke().charAt(0);
        },
    }
}
</script>

<style scoped>
.content {
    flex: 1;
    padding: 2rem;
    margin-left: 0;
    transition: margin-left 0.3s;
}

.user-info {
    display: flex;
    flex-direction: column;
    margin-left: 10px;
}

.avatar {
    background-color: #333;
    color: #fff;
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 20%;
    font-weight: bold;
    transition: transform 0.3s, margin-left 0.3s;
    font-size: xx-large;
}
</style>