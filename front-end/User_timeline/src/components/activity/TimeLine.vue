<template  v-if="fieldsChanged" >
  <div class="timeline-container relative flex flex-row gap-2.5 p-[18px] max-[600px]:flex-col max-[600px]:p-3 max-[600px]:pr-[30px] max-[600px]:gap-2">

    <div class="timeline-line absolute top-0 bottom-0 left-[35px] w-[1px] h-auto border-l-2 border-dashed border-graysecond -z-[2] max-[600px]:left-[28px]"></div>
    

    <div class="timeline-icon-cell">
      <div :class="[
        'timeline-icon-wrapper z-10 flex justify-center items-center rounded-full w-9 h-9 max-[600px]:w-7 max-[600px]:h-7',
        categoryClass
      ]">
        <component :is="icon" class="icon-only w-[26px] h-[26px]" stroke-width="1.5" />
      </div>
    </div>
    

<div :class="[
  'timeline-content bg-grayback rounded-[5px] border-l-4 h-auto p-[6px] ml-[10px] max-[600px]:w-full flex-grow',
  borderClass
]">


      <div class="timeline-header flex justify-between items-center pr-[5px] max-[600px]:flex-col max-[600px]:items-start max-[600px]:gap-1">
        <div class="timeline-action text-[17px] pl-[6px] max-[600px]:text-[15px]">
          {{ action }}
          <span v-if="targetUser?.username" class="user-tooltip relative font-medium cursor-pointer mx-[4px] max-[600px]:mx-[2px]"
                @mouseover="showTargetUserDetails = true"
                @mouseleave="showTargetUserDetails = false">
            {{ targetUser.username }}
            <div v-if="showTargetUserDetails" class="tooltip-box absolute top-full left-0 bg-white border border-graysecond p-[6px_10px] text-[12px] font-normal shadow-[0_2px_6px_rgba(0,0,0,0.15)] z-10 whitespace-nowrap">
              First name: {{ targetUser.firstName }}<br>
              Last name: {{ targetUser.lastName }}<br>
              Email: {{ targetUser.email }}
            </div>
          </span>
          by
          <span v-if="user?.username" class="user-tooltip relative font-medium cursor-pointer mx-[4px] max-[600px]:mx-[2px]"
                @mouseover="showUserDetails = true"
                @mouseleave="showUserDetails = false">
            {{ user.username }}
            <div v-if="showUserDetails" class="tooltip-box absolute top-full left-0 bg-white border border-graysecond p-[6px_10px] text-[12px] font-normal shadow-[0_2px_6px_rgba(0,0,0,0.15)] z-10 whitespace-nowrap">
              First name: {{ user.firstName }}<br>
              Last name: {{ user.lastName }}<br>
              Email: {{ user.email }}
            </div>
          </span>
        </div>
        <div class="timeline-dates text-[14px] text-graysecond max-[600px]:text-[12px] max-[600px]:pl-[7px]">
          <div>{{ relativeDate }}</div>
          <div>{{ exactDate }}</div>
        </div>
      </div>


      <div class="timeline-category-cell">
        <div :class="[
          'timeline-category-label text-[14px] w-[114px] h-[30px] flex justify-center items-center rounded-[20px] my-[4px] mt-[6px] max-[600px]:w-[93px] max-[600px]:ml-[8px] max-[600px]:text-[12px] max-[600px]:h-[26px]',
          categoryClass
        ]">
          <slot name="category">
            {{ category }}
          </slot>
        </div>
      </div>


      <div class="timeline-description-cell">
        <div class="timeline-description-text pl-[8px] p-[8px] max-[600px]:text-[12px]">
          <slot name="description">
            <span :class="[
              'timeline-dot inline-block w-1.5 h-1.5 rounded-full ml-1 align-middle max-[600px]:w-1 max-[600px]:h-1',
              dotColorClass
            ]"></span>
            {{ description }}
          </slot>
        </div>
      </div>

     <div 
      v-for="(change, field) in fieldsChanged"
      :key="field"
      class="inline-flex flex-wrap items-center m-[11px] mt-[9px] border-2 border-maincolor rounded-[34px] px-[9px] py-[2px] h-auto w-auto font-light max-[600px]:m-2 max-[600px]:mt-2 max-[600px]:px-1.5 max-w-full break-words whitespace-normal"
    >
      <strong class="field-name text-maincolor font-normal max-[600px]:text-[12px]">{{ field }}: </strong>
      <span class="text-black bg-lightred px-1 rounded line-through pl-[3px] font-light max-[600px]:text-[12px]">{{ change.old_val }}</span>
      <MoveRight class="change-icon relative top-[2px] w-[22px] stroke-[1.5] text-maincolor mx-[6px] max-[600px]:w-[18px] max-[600px]:mx-1" />
    <span class="text-black bg-lightgreen px-1 rounded pl-[2px] font-light max-[600px]:text-[12px]">{{ change.new_val }}</span>
    </div>

    </div>
  </div>
</template>


<script setup>
import { ref, computed } from 'vue'    
import { MoveRight } from 'lucide-vue-next';

const props = defineProps({
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
    default: () => ({})
  },
  isAuthLog: {
    type: Boolean,
    default: false
  },
  category: {
    type: String,
    default: ''
  },
  fieldsChanged: {
    type: Object,
    default: null
  },
  relativeDate: {
    type: String,
    default: ''
  },
  exactDate: {
    type: String,
    default: ''
  },
})

const showUserDetails = ref(false)
const showTargetUserDetails = ref(false)

const categoryClass = computed(() => {
  switch (props.category.toLowerCase()) {
    case 'authentication': return 'text-darkbrown bg-lightbrown'
    case 'management': return 'text-maincolor bg-lightblue'
    default: return ''
  }
})

const borderClass = computed(() => {
  switch (props.category.toLowerCase()) {
    case 'authentication': return 'border-l-darkbrown'
    case 'management': return 'border-l-maincolor'
    default: return ''
  }
})

const dotColorClass = computed(() => {
  switch (props.category.toLowerCase()) {
    case 'authentication': return 'bg-darkbrown'
    case 'management': return 'bg-maincolor'
    default: return ''
  }
})
</script>
