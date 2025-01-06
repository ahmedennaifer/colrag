<template>
  <div class="fullscreen bg-red text-white text-center q-pa-md flex flex-center">
    <div>
      <div style="font-size: 30vh">
        404  DAMMMIT !!!

      </div>

      <!-- <div class="text-h1" style="opacity:.4; color: red; ">
        DAMMMIT !!!
      </div> -->

      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="red"
        unelevated
        to="/"
        label="Go Home"
        no-caps
      />
    </div>
  </div>
</template>

<script setup>
defineOptions({
  name: 'ErrorNotFound'
});
</script>
