// ==============================================================================
// Supabase Configuration
// ==============================================================================
// 1. Go to https://supabase.com/dashboard
// 2. Select your project -> Project Settings -> API
// 3. Copy your "Project URL" and "anon / public" API key below:

const SUPABASE_URL = 'https://tcecypcrmemdtqcwoojt.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_MZ80JSkeWuRfwwFeP4YpvQ_FzTU92wP';

/**
 * Checks if Supabase credentials have been configured.
 */
function isSupabaseConfigured() {
    return (
        SUPABASE_URL &&
        SUPABASE_URL !== 'YOUR_SUPABASE_URL' &&
        SUPABASE_ANON_KEY &&
        SUPABASE_ANON_KEY !== 'YOUR_SUPABASE_ANON_KEY'
    );
}

// Initialize the Supabase client if the SDK is loaded and credentials are set
let supabaseClient = null;
if (typeof window !== 'undefined' && window.supabase) {
    if (isSupabaseConfigured()) {
        supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    }
}

// Expose client to global scope
window.sbClient = supabaseClient;
window.isSupabaseConfigured = isSupabaseConfigured;
