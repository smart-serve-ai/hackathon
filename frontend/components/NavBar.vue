<script setup>
const route = useRoute();
</script>

<template>
  <nav class="navbar navbar-expand-md navbar-light bg-light">
    <div class="container">
      <NuxtLink class="navbar-brand" to="/"> SmartServe </NuxtLink>

      <button
        id="navbar-toggler"
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbar-collapse"
      >
        <!-- <font-awesome-icon icon="fa-solid fa-bars" /> -->
      </button>

      <div id="navbar-collapse" class="collapse navbar-collapse justify-content-end">
        <ul class="navbar-nav">
          <li class="nav-item">
            <NuxtLink
              class="nav-link"
              :class="{ active: route.path.startsWith('/dashboard/goals') }"
              to="/dashboard/goals"
            >
              Goals
            </NuxtLink>
          </li>

          <li class="nav-item">
            <NuxtLink class="nav-link" to="/user/logout"> Logout </NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
