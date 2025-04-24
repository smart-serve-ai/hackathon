<script setup>
const userStore = useUserStore();

const title = ref("");
const description = ref("");

const errorMessages = ref([]);

const handleAddGoal = async () => {
  try {
    const response = await $fetch("/api/v1/dashboard/add-goal", {
      method: "POST",
      body: {
        title: title.value,
        description: description.value,
        user_id: userStore.id,
      },
    });

    navigateTo("/dashboard/goals");
  } catch (error) {
    const { status, data } = error;

    if (data && data.detail) {
      errorMessages.value =
        typeof data.detail === "string" ? [data.detail] : data.detail;
    }
  }
};
</script>

<template>
  <div class="container">
    <ErrorMessages v-if="errorMessages.length" :errorMessages="errorMessages" class="my-3" />

    <h1 class="my-4">Add New Goal</h1>

    <div class="mb-3">
      <label for="title" class="form-label">Title</label>
      <input
        id="title"
        v-model="title"
        type="text"
        placeholder="Enter goal title"
        required
        class="form-control"
      />
    </div>

    <div class="mb-3">
      <label for="description" class="form-label">Description</label>
      <textarea
        id="description"
        v-model="description"
        placeholder="Describe your goal"
        rows="4"
        required
        class="form-control"
      ></textarea>
    </div>

    <button type="submit" class="btn btn-primary w-100" @click="handleAddGoal">
      Add Goal
    </button>
  </div>
</template>
