<script setup>
const userStore = useUserStore();
onMounted(() => {
  if (!userStore.id) {
    navigateTo("/user/enter-phone");
  } else {
    navigateTo("/dashboard/goals");
  }
});
</script>
<template></template>
