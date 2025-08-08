<template>
  <div class="timeline">
  <div class="timeline-line"></div>
  <div class="timeline-icon-cell">
    <div class="timeline-icon" :class="category.toLowerCase()">
      <component :is="icon" class="icon-only" stroke-width="1.5" />
    </div>
  </div>
  
  <div class="timeline-right-container" :class="category.toLowerCase()">

    <!-- <div class="timeline-content-cell">
      <div class="timeline-content">
        <slot />
      </div>
    </div> -->
    <div class="first-row">
      <div class="action-title">
        {{ action }}

        <span v-if="targetUser?.username" class="username-wrapper"
              @mouseover="showTargetUserDetails = true"
              @mouseleave="showTargetUserDetails = false"
        >
          {{ targetUser.username }}
          <div v-if="showTargetUserDetails" class="tooltip">
            First name: {{ targetUser.firstName }}<br>
            Last name: {{ targetUser.lastName }}<br>
            Email: {{ targetUser.email }}
          </div>
        </span>

        by

        <span v-if="user?.username" class="username-wrapper"
              @mouseover="showUserDetails = true"
              @mouseleave="showUserDetails = false"
        >
          {{ user.username }}
          <div v-if="showUserDetails" class="tooltip">
            First name: {{ user.firstName }}<br>
            Last name: {{ user.lastName }}<br>
            Email: {{ user.email }}
          </div>
        </span>
      </div>

      <div class="timeline-date-cell">
        <div class="timeline-date">
            <div>{{ relativeDate }}</div>
            <div>{{ exactDate }}</div>
        </div>
      </div>
    </div>


    <div class="timeline-category-cell">
      <div class="timeline-category" :class="category.toLowerCase()">
        <slot name="category">
          {{ category }}
        </slot>
      </div>
    </div>


    <div class="timeline-description-cell">
      <div class="timeline-description">
        <slot name="description">
          <span class="dot" :class="category.toLowerCase()"></span>
          {{ description }}
        </slot>
      </div>
    </div>
    

    <div v-if="fieldsChanged" class="timeline-fields-cell">
      <div v-for="(change, field) in fieldsChanged" :key="field" class="timeline-fields">
        <strong class="field">{{ field }}: </strong>

        <span class="old-val">{{ change.old_val }}</span>

        <MoveRight class="change-icon" />
        
        <span class="new-val">{{ change.new_val }}</span>
      </div>
    </div>





  </div>

  </div>
</template>



<script setup>
import { ref } from 'vue'
import { MoveRight } from 'lucide-vue-next';

defineProps({
    date: {
        type: String,
        default: '',
    },

    icon: {
      type: [Object, Function],
      required: true
    },

    description: {
        type: String,
        default: '',
    },

    user: {
    type: Object,
    default: () => ({})
    },
      action: {
    type: String,
    default: '',
    },
    targetUser: {
       type: Object,
      default: () => ({}) },

    isAuthLog: {
      type: Boolean,
      default: false
   },

    category: { type: String, default: '' },      
    fieldsChanged: { type: Object, default: null }, 
    relativeDate: { type: String, default: '' },    
    exactDate: { type: String, default: '' },  

})
const showUserDetails = ref(false)
const showTargetUserDetails = ref(false)
</script>

<style lang="scss">
@import "../../style/variables";

.timeline{
  position: relative;
  display: flex;
  flex-direction: row;
  gap: 10px;
  padding: 18px;
}
.timeline-line {
  position: absolute;
  top: 0;
  bottom: 0;
  left:35px;  
  width: 0.5%;
  height: auto;
  border-left: 2px dashed #ccc;
  z-index: -2;
}

.timeline-right-container{
  background-color: $grayback;
  border-radius: 5px;
  border-left: 4px solid;
  height: auto;
  width: 90%;
  padding: 6px;
  margin-left: 10px;
  &.authentication{
    border-left-color: $darkbrown;
  }

  &.management{
    border-left-color: $maincolor;
  }
  
}

.timeline-icon {
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 100%;
  width: 36px; 
  height: 36px; 
  
  &.authentication{
    color: $darkbrown;
    background-color: $lightbrown;
  }

  &.management{
    color: $maincolor;
    background-color: $lightblue;

  }
  
  
  .icon-only {
    width: 26px;
    height: 26px;
  }
}



.first-row{
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.timeline-date-cell {
  font-size: 14px;
  color: $grayfont;
}

.action-title{
  font-size: 17px;
  
  .username-wrapper {
  position: relative;
  font-weight: 500;
  cursor: pointer;
  margin: 0 4px;
}

.tooltip {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid #ccc;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 400;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  z-index: 10;
  white-space: nowrap;
}

}

.timeline-category{
  font-size: 14px;
  width: 114px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 20px;
  margin: 4px;
  margin-top: 6px;

  &.authentication{
    color: $darkbrown;
    background-color: $lightbrown;
  }

  &.management{
    color: $maincolor;
    background-color: $lightblue;

  }
  
}

.timeline-description{
  padding-left: 8px;
  padding: 8px;
}

.dot {
  width: 5px;
  height: 5px;
  border-radius: 100%;
  display: inline-block;
  margin-left: 4px;
  vertical-align: middle;

  &.authentication {
    background-color: $darkbrown;
  }

  &.management {
    background-color: $maincolor;
  }
}

.timeline-fields{
  display: inline-flex;
  align-items: center;
  margin: 11px;
  margin-top: 9px;
  border: 2px solid $maincolor;
  border-radius: 34px;
  padding: 1px;
  padding-left: 9px;
  padding-right: 9px;
  height: 24px;
  width: auto;
  font-weight: lighter;
  .field{
    color: $maincolor;
    font-weight: 400;
  }
  .old-val{
    color: red;
    text-decoration: line-through;
    padding-left: 3px;
    font-weight: 300;
  }

  .new-val{
    color: #00A34C;
    padding-left: 2px;
    font-weight:300;
  }

  .change-icon {
    position: relative;
    top: 2px; 
    size: 22px;
    stroke-width: 1.5px;
    color: $maincolor;
    margin: 0 6px;
  }
}


</style>
َ