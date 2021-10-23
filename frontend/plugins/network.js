export default ({store}) => {
  window.addEventListener('online', function() {
    store.commit('changeStatusToOnline')
  })

  window.addEventListener('offline', function() {
    store.commit('changeStatusToOffline')
  })
}