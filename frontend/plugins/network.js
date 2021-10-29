export default ({store, app}) => {
  window.addEventListener('online', function() {
    store.commit('changeStatusToOnline')
    app.$sync()
  })

  window.addEventListener('offline', function() {
    store.commit('changeStatusToOffline')
  })
}