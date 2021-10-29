export default ({store}) => {
  if (store.state.completePreload) {
    // 何もしない
    return true
    
  } else {
    // まだ初回のロードがされていない場合
    Promise.all([
      store.dispatch('fetchAndApplyTasks'),
      store.dispatch('fetchAndApplyCategoryData')
    ])
    .then(() => {
      store.commit('completePreload')
    })
  }
}