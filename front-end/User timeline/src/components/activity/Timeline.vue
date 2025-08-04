<template>
  <tr class="timeline">
    <td class="timeline-icon-cell">
      <div class="timeline-icon">
        <slot name="icon">
          {{ icon }}
        </slot>
      </div>
    </td>

    <td class="timeline-content-cell">
      <div class="timeline-content">
        <slot />
      </div>
    </td>

    <td class="timeline-date-cell">
      <div class="timeline-date">
        <slot name="date">
          {{ date }}
        </slot>
      </div>
    </td>

    <td class="timeline-action-cell">
      <div class="timeline-action">
        <slot name="action">
          {{ action }}
        </slot>
      </div>
    </td>


    <!-- <td class="timeline-targetuser-cell">
      <div class="timeline-targetuser">
        <slot name="targetuser">
          {{ targetuser }}
        </slot>
      </div>
    </td> -->

    <td class="timeline-tuser-cell">
      <div class="timeline-user">
        <slot name="user">
          {{ user }}
        </slot>
      </div>
    </td>


    <td class="timeline-description-cell">
      <div class="timeline-description">
        <slot name="description">
          {{ description }}
        </slot>
      </div>
    </td>
  </tr>
</template>

<script setup>
defineProps({
    date: {
        type: String,
        default: '',
    },
    icon: {
        type: String,
    },
    description: {
        type: String,
        default: '',
    },
    user: {
    type: Object,
    default: ({})
    },
      action: {
    type: String,
    default: '',
    },
})
</script>

<style></style>
