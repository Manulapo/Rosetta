<template>
  <div class="clean-component">
    <!-- Clean translations with no conflicts or redundancy -->
    <h1>{{ $t('app.title', 'My Application') }}</h1>
    <p>{{ t('app.description', 'A simple test application') }}</p>
    <button>{{ $t('actions.submit', 'Submit Form') }}</button>
    <span>{{ t('status.ready', 'Ready to proceed') }}</span>
  </div>
</template>

<script>
export default {
  name: 'CleanComponent',
  mounted() {
    console.log(this.$t('messages.success', 'Operation completed'));
  }
}
</script>