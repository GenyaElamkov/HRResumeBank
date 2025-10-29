document.addEventListener('DOMContentLoaded', function() {
    if (!sessionStorage.getItem('betaWarningShown')) {
        var betaModal = new bootstrap.Modal(document.getElementById('betaWarningModal'));
        betaModal.show();

        sessionStorage.setItem('betaWarningShown', 'true');
    }
});
