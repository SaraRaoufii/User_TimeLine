import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import jwt_decode from 'jwt-decode'
import gql from 'graphql-tag'
import apolloClient from '@/apollo/client'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref({})
  const username = ref('')
  const token = ref('')
  const isLoggedIn = ref(false)
  const isLoading = ref(false)
  const router = useRouter()

  const GET_ME = gql`
    query Me {
      me {
        id
        username
        firstName
        lastName
        email
        phone
        address
        role
        isStaff
        isActive
      }
    }
  `
  function setUser(data) {
    currentUser.value = { ...data }
    username.value = data.username
    token.value = data.token || ''
    isLoggedIn.value = true
  }

  async function checkLogin() {
    const storedToken = localStorage.getItem('token')
    if (!storedToken) {
      isLoggedIn.value = false
      return false
    }
    try {
      const decoded = jwt_decode(storedToken)
      token.value = storedToken
      isLoggedIn.value = true
      username.value = decoded.username
      return true
    } catch {
      logout()
      return false
    }
  }

  async function fetchUserData() {
    try {
      const { data } = await apolloClient.query({
        query: GET_ME,
        fetchPolicy: 'network-only',
        context: {
          headers: { Authorization: `Bearer ${token.value}` }
        }
      })
      if (data?.me) {
        currentUser.value = { ...data.me, token: token.value }
        username.value = data.me.username
        return true
      }
      return false
    } catch (err) {
      console.error('Error fetching user data:', err)
      logout()
      return false
    }
  }
  async function initUser() {
    isLoading.value = true
    const loggedIn = await checkLogin()
    if (loggedIn) {
      await fetchUserData()
    }
    isLoading.value = false
  }

  function logout() {
    localStorage.removeItem('token')
    currentUser.value = {}
    username.value = ''
    token.value = ''
    isLoggedIn.value = false
    router.push('/login')
  }

  return { 
    currentUser, username, token, isLoggedIn, isLoading,
    setUser, checkLogin, fetchUserData, initUser, logout
  }
})
