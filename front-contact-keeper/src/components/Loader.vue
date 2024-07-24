
<template>
  <div class="back-loader">
    <div class="loader"></div>
  </div>
</template>
<script >
export default {

}
</script>
<style scoped>

.loader {
  position: relative;
  width: 180px;
  height: 130px;
  margin: 0 auto;
}
.loader:before {
  content: "";
  position: absolute;
  bottom: 70px;
  left: 20px;
  height: 50px;
  width: 50px;
  border-radius: 50%;
  background: white;
  animation: loading-bounce 0.5s ease-in-out infinite alternate;
}
.loader:after {
  content: "";
  position: absolute;
  right: 0;
  top: 0;
  height: 17px;
  width: 100px;
  border-radius: 4px;
  box-shadow: 0 70px 0 #fff, -75px 50px 0 #fff, -70px 95px 0 #fff;
  animation: loading-step 1s ease-in-out infinite;
}

@keyframes loading-bounce {
  0% { transform: scale(1, 0.7)}
  40% { transform: scale(0.8, 1.2)}
  60% { transform: scale(1, 1)}
  100% { bottom: 140px }
}
@keyframes loading-step {
  0% {
    box-shadow: 0 70px 0 rgba(0,0,0,0),
    0 20px 0 #fff,
    -75px 50px 0 #fff,
    -130px 90px 0 #fff;
  }
  100% {
    box-shadow: 0 20px 0 #fff,
    -75px 50px 0 #fff,
    -130px 90px 0 #fff,
    -150px 90px 0 rgba(0,0,0,0);
  }
}


.back-loader{
  position:absolute;
  background-color: rgba(0,0,0, 0.06);
  display:flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  opacity: 40%;
}
</style>