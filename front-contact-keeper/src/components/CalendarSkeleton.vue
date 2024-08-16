<template>
    <div class="skeleton-calendar">
      <div class="skeleton-header">
        <div class="skeleton-button"></div>
        <div class="skeleton-button"></div>
        <div class="skeleton-button"></div>
        <div class="skeleton-button"></div>
      </div>
      <div class="skeleton-header">
        <div class="skeleton-nav-button"></div>
        <div class="skeleton-title"></div>
        <div class="skeleton-nav-button"></div>
      </div>
      <div class="skeleton-grid">
        <div class="skeleton-day-header" v-for="i in 7"></div>
        <div class="skeleton-day" v-for="i in 7"></div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'CalendarSkeleton',
  };
  </script>
  
  <style scoped>
  .skeleton-calendar {
    width: 100%;
    height: 70vh;
    background-color: #f8f8f8ef;
    border-radius: 3px;
    padding: 20px;
    box-sizing: border-box;
  }
  
  .skeleton-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .skeleton-button,
  .skeleton-nav-button,
  .skeleton-title,
  .skeleton-day-header,
  .skeleton-day {
    background-color: #e0e0e0;
    border-radius: 4px;
    animation: pulse 1.5s infinite ease-in-out;
  }
  
  .skeleton-button {
    width: 80px;
    height: 40px;
    margin-right: 10px;
  }
  
  .skeleton-nav-button {
    width: 40px;
    height: 40px;
  }
  
  .skeleton-title {
    width: 150px;
    height: 40px;
  }
  
  .skeleton-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 10px;
    height: calc(100vh - 140px);
  }
  
  .skeleton-day-header {
    width: 100%;
    height: 20px;
    margin-bottom: 10px;
  }
  
  .skeleton-day {
    width: 100%;
    height: 100px;
  }
  
  @keyframes pulse {
    0% {
      background-color: #e0e0e0;
    }
    50% {
      background-color: #f0f0f0;
    }
    100% {
      background-color: #e0e0e0;
    }
  }
  </style>
  