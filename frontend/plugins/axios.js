export default function ({ $axios, redirect, $auth }) {
  // $axios.onRequest((config) => {
  // })

  $axios.onError((error) => {
    const code = parseInt(error.response.status)
    if (code === 401) {
      $auth.logout()
      redirect('/401')
    }
  })
}
