import React from "react";

function formatTime(minutes) {
  const hours = Math.floor(minutes / 60);
  const mins = Math.floor(minutes % 60);
  if (hours > 0) {
    return `${hours}h ${mins}m`;
  }
  return `${mins}m`;
}

function Overview({ overview }) {
  if (!overview) return <div>Loading...</div>;

  const winRate = (overview.wins / overview.total_runs * 100).toFixed(1);
  const losses = overview.total_runs - overview.wins;
  const avgTime = formatTime(overview.playtime / overview.total_runs);
  const formattedTime = formatTime(overview.playtime);

  return (
    <div>
      <h2>Overview</h2>

      <p>Total Runs: {overview.total_runs}</p>
      <p>Wins: {overview.wins}</p>
      <p>Losses: {losses}</p>
      <p>Win Rate: {winRate}%</p>

      <p>Total Playtime: {formattedTime}</p>
      <p>Average Run Time: {avgTime}</p>
    </div>
  );
}

export default Overview;