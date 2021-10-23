export const state = () => ({
  online: window.navigator.onLine,
})

export const mutations = {
  changeStatusToOnline(state) {
    state.online = true
    console.log('online now')
  },
  changeStatusToOffline(state) {
    state.online = false
    console.log('offline now')
  }
}

export const getters = {
  isOnline(state) {
    return state.online;
  }
}