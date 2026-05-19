<script setup>
import { computed, onMounted, ref } from 'vue'

const props = defineProps({
  title: { type: String, default: 'Vue sur /home' },
  initialCount: { type: Number, default: 0 },
  initialName: { type: String, default: '' },
})

const count = ref(props.initialCount)
const name = ref(props.initialName)
const nameInput = ref(null)

const greeting = computed(() => (name.value.trim() ? `Salut ${name.value}` : 'Salut'))

const increment = () => {
  count.value += 1
}

const reset = () => {
  count.value = props.initialCount
  name.value = props.initialName
  nameInput.value?.focus()
}

onMounted(() => {
  nameInput.value?.focus()
})
</script>

<template>
  <article>
    <header>
      <strong>{{ title }}</strong>
    </header>

    <div class="grid">
      <label>
        Nom
        <input ref="nameInput" v-model.trim="name" placeholder="Ton prénom" />
      </label>

      <div>
        <p style="margin-bottom: 0.5rem">{{ greeting }}</p>
        <p style="margin-bottom: 0.5rem">
          Compteur: <strong>{{ count }}</strong>
        </p>

        <div role="group">
          <button type="button" @click="increment">+1</button>
          <button type="button" class="secondary" @click="reset">Reset</button>
        </div>
      </div>
    </div>
  </article>
</template>
