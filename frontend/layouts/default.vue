<template>
    <div class="d-flex flex-column h-100">
      <NuxtLoadingIndicator />
      <NavBar />
  
      <div>
        <slot />
      </div>
  
      <!-- <div class="mt-auto">
        <Footer />
      </div> -->
    </div>
  </template>