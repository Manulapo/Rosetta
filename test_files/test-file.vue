<template>
  <div class="test-component">
    <!-- Normal translations -->
    <h1>{{ $t('welcome.title', 'Welcome to Our App') }}</h1>
    <p>{{ t('welcome.message', 'This is a test application') }}</p>
    
    <!-- Duplicate key error - same key with different values -->
    <button>{{ $t('button.save', 'Save Changes') }}</button>
    <span>{{ $t('button.save', 'Save Document') }}</span>
    
    <!-- Redundancy error - different keys with same value -->
    <div>{{ t('loading.text', 'Loading...') }}</div>
    <div>{{ $t('spinner.message', 'Loading...') }}</div>
    
    <!-- Pattern redundancy - same dynamic pattern -->
    <p>{{ $t('user.welcome', 'Hello {name}!') }}</p>
    <p>{{ t('greeting.user', 'Hello {username}!') }}</p>
  </div>
</template>

<script setup>
</script>