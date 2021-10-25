export default ({store}) => {
  window.addEventListener('load', function() {
    console.log('event: load')
    store.dispatch('fetchAndApplyTasks')
  })
}