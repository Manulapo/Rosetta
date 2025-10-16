<template>
  <h1>{{ t('app.title', 'My Application') }}</h1>
  <p>{{ $t('app.description', 'A simple test application') }}</p>
  <button>{{ t('actions.submit', 'Submit Form') }}</button>
  <span>{{ $t('status.ready', 'Ready to proceed') }}</span>
</template>

<script setup>
</script>