select "title", count(votes.post_id) as num_votes from posts left join votes on id = votes.post_id group by "title";
