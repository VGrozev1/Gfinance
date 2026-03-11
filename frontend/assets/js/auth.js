/**
 * Supabase Auth helpers.
 * Load supabase-config.js and @supabase/supabase-js before this.
 */
(function () {
  'use strict';
  if (typeof window.supabase === 'undefined') return;
  var supabase = window.supabase;

  window.getAuthToken = function () {
    return supabase.auth.getSession().then(function (r) {
      return r.data?.session?.access_token || null;
    });
  };

  window.auth = {
    getSession: function () {
      return supabase.auth.getSession();
    },
    getUser: function () {
      return supabase.auth.getUser();
    },
    signIn: function (email, password) {
      return supabase.auth.signInWithPassword({ email: email, password: password });
    },
    signUp: function (email, password, opts) {
      return supabase.auth.signUp({ email: email, password: password, options: opts || {} });
    },
    signOut: function () {
      return supabase.auth.signOut();
    },
    onAuthStateChange: function (cb) {
      return supabase.auth.onAuthStateChange(cb);
    },
    getAccessToken: function () {
      return supabase.auth.getSession().then(function (r) {
        return r.data?.session?.access_token || null;
      });
    },
  };
})();
