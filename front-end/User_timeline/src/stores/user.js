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
        isLocked
        isActive
      }
    }
  `

const REFRESH_TOKEN = gql`
mutation RefreshToken($token: String!) {
  refreshToken(token: $token) {
    token
    payload
    refreshExpiresIn
  }
}
`

const LOGOUT_MUTATION = gql`
  mutation LogoutUser {
    logoutUser {
      success
      message
    }
  }
`

function setUser(data) {
  currentUser.value = { ...data }
  username.value = data.username
  token.value = data.token || ''
  localStorage.setItem('token', token.value)
  if (data.refreshToken) {
    localStorage.setItem('refresh_token', data.refreshToken)
  }
  isLoggedIn.value = true
}

async function refreshTokenIfNeeded() {
  const storedToken = localStorage.getItem('token')
  if (!storedToken) return false

  const decoded = jwt_decode(storedToken)
  const now = Date.now() / 1000

const REFRESH_THRESHOLD = 30 
if (decoded.exp && decoded.exp < now + REFRESH_THRESHOLD) {
    const refresh = localStorage.getItem('refresh_token')
    if (!refresh) {
      logout()
      return false
    }
    try {
      const { data } = await apolloClient.mutate({
        mutation: REFRESH_TOKEN,
        variables: { token: refresh },
      })
      const newToken = data.refreshToken.token

      localStorage.setItem('token', newToken)
      token.value = newToken
      username.value = jwt_decode(newToken).username
      return true
    } catch (err) {
      const { useAlertStore } = await import('@/stores/alert')
      const alertStore = useAlertStore()
      alertStore.show('Session expired. Please login again.', 'warning')
      logout()
      return false
    }
  }

  return true
}



async function checkLogin() {
  const storedToken = localStorage.getItem('token')
  if (!storedToken) {
    isLoggedIn.value = false
    return false
  }

  try {
    const ok = await refreshTokenIfNeeded()
    if (!ok) return false

    token.value = localStorage.getItem('token')
    const decoded = jwt_decode(token.value)
    isLoggedIn.value = true
    username.value = decoded.username
    return true
  } catch (err) {
    const { useAlertStore } = await import('@/stores/alert')
    const alertStore = useAlertStore()
    alertStore.show('Session expired. Please login again.', 'warning')
    logout()
    return false
  }
}



async function fetchUserData() {
  const ok = await refreshTokenIfNeeded()
  if (!ok) return false

  token.value = localStorage.getItem('token') 

  try {
    const { data } = await apolloClient.query({
      query: GET_ME,
      fetchPolicy: 'network-only',
      context: { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
    })

    if (data?.me) {
      currentUser.value = { ...data.me, token: token.value }
      username.value = data.me.username
      return true
    }
    return false
  } catch (err) {
    const { useAlertStore } = await import('@/stores/alert')
    const alertStore = useAlertStore()
    alertStore.show('Cannot fetch user data. Please login again.', 'error')
    logout()
    return false
  }
}



  async function initUser() {
    isLoading.value = true
    const loggedIn = await checkLogin()
    if (loggedIn) {
      const ok = await fetchUserData()
      if (!ok) isLoggedIn.value = false
    }
    isLoading.value = false
    setInterval(async () => {
  if (isLoggedIn.value) {
    await refreshTokenIfNeeded()
  }
}, 30000)
  }

async function logout() {
  try {
    if (!token.value) {
      console.warn('No token, skipping logout mutation')
    } else {
      await apolloClient.mutate({
        mutation: LOGOUT_MUTATION,
        context: { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      })

    }
  } catch (err) {
    console.error('Logout mutation failed', err)
  } finally {
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
    currentUser.value = {}
    username.value = ''
    token.value = ''
    isLoggedIn.value = false
    router.push('/login')
  }
}

  return {
    currentUser,
    username,
    token,
    isLoggedIn,
    isLoading,
    setUser,
    checkLogin,
    fetchUserData,
    initUser,
    logout
  }
})