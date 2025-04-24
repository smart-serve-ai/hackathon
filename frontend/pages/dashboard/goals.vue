<script setup>
import { camelizeKeys } from "humps";

const userStore = useUserStore();

const goals = ref([]);

const errorMessages = ref([]);

const fetchGoals = async () => {
  errorMessages.value = [];

  try {
    const response = await $fetch(
      `/api/v1/dashboard/goals?user_id=${userStore.id}`,
      {
        method: "GET",
      }
    );
    goals.value = camelizeKeys(response.goals);
  } catch (error) {
    const { status, data } = error;

    if (data && data.detail) {
      errorMessages.value =
        typeof data.detail === "string" ? [data.detail] : data.detail;
    }
  }
};

onMounted(() => {
  fetchGoals();
});
</script>
<template>
  <div class="container">
    <ErrorMessages
      v-if="errorMessages.length"
      :errorMessages="errorMessages"
      class="my-3"
    />

    <div v-for="goal in goals" :key="goal.id" class="card my-3">
      <div class="card-header">
        <h6 class="my-1">{{ goal.title }}</h6>
      </div>
      <div class="card-body">
        {{ goal.description }}
      </div>

      <div v-if="goal.conversationHistory?.length" class="card-footer bg-transparent py-3">
          <div class="d-flex flex-column gap-2">
            <div
              v-for="(msg, index) in goal.conversationHistory"
              :key="index"
              :class="[
                'd-flex',
                msg.role === 'assistant'
                  ? 'justify-content-end'
                  : 'justify-content-start',
              ]"
              class="my-3"
            >
              <div
                :class="[
                  'p-3',
                  'rounded-3',
                  'shadow-sm',
                  'position-relative',
                  msg.role === 'assistant'
                    ? 'bg-primary text-white'
                    : 'bg-light',
                  msg.role === 'assistant' ? 'me-2' : 'ms-2',
                ]"
                style="max-width: 75%"
              >
                <div class="small mb-1 fw-bold">
                  {{
                    msg.role === "assistant" ? "Agentic AI" : "Service Provider"
                  }}
                </div>
                <div>
                  {{ msg.content }}
                </div>
              </div>
            </div>
          
        </div>
      </div>
    </div>

    <div class="mt-3">
      <NuxtLink class="btn btn-primary" to="/dashboard/add-goal">
        Add Goal
      </NuxtLink>
    </div>
  </div>
</template>
