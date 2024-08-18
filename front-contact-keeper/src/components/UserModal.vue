<template>
    <Dialog header="Informacion del Usuario" :modal="true" :closeOnEscape="false" :closable="false" position="center"
        :contentStyle="{ overflow: 'visible' }" :visible.sync="visible" @click="close">

        <div class="user-info-container">
            <div class="avatar">{{ getAvatarLetter() }}</div>
            <p class="user-name"><strong>Nombre:</strong> {{ name }}</p>
            <p class="user-email"><strong>Correo:</strong> {{ email }}</p>
        </div>
        <div class="button-container">
            <Button label="Cerrar" class="p-button-text p-button-text p-button-plain" @click="close()" />
        </div>
    </Dialog>
</template>

<script>
import Button from 'primevue/button/Button';
import Dialog from 'primevue/dialog/Dialog';
import utils from '@/kernel/utils';
export default {
    props: {
        visible: {
            type: Boolean,
            required: true
        },
        name: {
            type: String,
            required: true
        },
        email: {
            type: String,
            required: true
        }
    },
    methods: {
        close() {
            this.$emit('close');
        },
        getAvatarLetter() {
            return utils.getUserFromToke().charAt(0);
        },
    }
}
</script>

<style scoped>
.user-info-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 20px;
}

.button-options {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
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
}

.user-name {
    font-size: 18px;
    margin-bottom: 10px;
}

.user-email {
    font-size: 16px;
    color: #666;
}

.button-container {
    display: flex;
    justify-content: flex-end;
    padding: 10px 20px 0 20px;
}
</style>