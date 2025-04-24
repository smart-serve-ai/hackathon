<script setup>
definePageMeta({
  layout: false,
});

const userStore = useUserStore();

const code = ref("");
const errorMessages = ref([]);

const handleVerifyOTP = async () => {
  try {
    const response = await $fetch("/api/v1/user/verify-otp", {
      method: "POST",
      body: {
        phone: userStore.phone,
        phone_code_hash: userStore.phoneCodeHash,
        code: code.value,
      },
    });
    console.log(response);

    userStore.id = response.user_id;

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
    
    <div class="row justify-content-center py-5">
      <div class="col-md-6">
        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <label for="phone" class="form-label">Enter OTP</label>
            <input type="text" id="code" v-model="code" class="form-control" />
          </div>
          <button
            type="submit"
            class="btn btn-primary w-100"
            @click="handleVerifyOTP"
          >
            Verify
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
