<template>
  <div class="chat-skeleton">
    <b-row>
      <b-col cols="12" class="d-flex justify-content-end">
        <div class="w-75 chat-content-skeleton">
          <div class="chat-username-skeleton shimmer"></div>
          <div class="chat-message-skeleton large shimmer"></div>
        </div>
      </b-col>
      <b-col cols="12" class="d-flex justify-content-start">
        <div class="w-75 chat-content-skeleton">
          <div class="chat-username-skeleton shimmer"></div>
          <div class="chat-message-skeleton large shimmer"></div>
        </div>
      </b-col>
      <b-col cols="12" class="d-flex justify-content-end">
        <div class="w-75 chat-content-skeleton">
          <div class="chat-username-skeleton shimmer"></div>
          <div class="chat-message-skeleton large shimmer"></div>
        </div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  name: 'ChatSkeleton',
};
</script>

<style scoped>
.chat-skeleton {
  padding: 10px;
}

.chat-content-skeleton {
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 15px;
  max-width: 80%;
  position: relative;
}

.chat-username-skeleton {
  height: 12px;
  width: 30%;
  background-color: #d0d0d0;
  margin-bottom: 0.5rem;
  border-radius: 4px;
}

.chat-message-skeleton.large {
  height: 20px;
  width: 100%;
  background-color: #e0e0e0;
  border-radius: 4px;
}

.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
