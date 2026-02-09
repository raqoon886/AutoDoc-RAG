(function() {
    var implementors = Object.fromEntries([["tokio_util",[["impl&lt;L, R, Item, Error&gt; Sink&lt;Item&gt; for <a class=\"enum\" href=\"tokio_util/either/enum.Either.html\" title=\"enum tokio_util::either::Either\">Either</a>&lt;L, R&gt;<div class=\"where\">where\n    L: Sink&lt;Item, Error = Error&gt;,\n    R: Sink&lt;Item, Error = Error&gt;,</div>"],["impl&lt;T: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.93.0/core/marker/trait.Send.html\" title=\"trait core::marker::Send\">Send</a>&gt; Sink&lt;T&gt; for <a class=\"struct\" href=\"tokio_util/sync/struct.PollSender.html\" title=\"struct tokio_util::sync::PollSender\">PollSender</a>&lt;T&gt;"]]]]);
    if (window.register_implementors) {
        window.register_implementors(implementors);
    } else {
        window.pending_implementors = implementors;
    }
})()
//{"start":57,"fragment_lengths":[620]}