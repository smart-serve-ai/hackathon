<script setup>
definePageMeta({
  layout: false,
});

const userStore = useUserStore();

const phone = ref("");
const errorMessages = ref([]);

const handleSendOTP = async () => {
  console.log("Sending OTP...");

  try {
    const response = await $fetch("/api/v1/user/send-otp", {
      method: "POST",
      body: {
        phone: phone.value,
      },
    });

    userStore.phone = phone.value;
    userStore.phoneCodeHash = response.phone_code_hash;

    console.log(response);
    navigateTo("/user/verify-otp");
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
            <label for="phone" class="form-label">Phone Number</label>
            <input
              type="text"
              id="phone"
              v-model="phone"
              class="form-control"
            />
          </div>
          <button
            type="submit"
            class="btn btn-primary w-100"
            @click="handleSendOTP"
          >
            Send OTP
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
