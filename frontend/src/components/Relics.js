import React, { useState } from "react";

function Relics({ relics }) {
    const [sortKey, setSortKey] = useState("id");
    const [ascending, setAscending] = useState(false);
    const sorted = Object.entries(relics).sort((a, b) => { // sort the data by specified parameter
        if (sortKey === "id") { // if sorting by name
            return ascending
                ? a[0].localeCompare(b[0])
                : b[0].localeCompare(a[0]);
        }

        let valA, valB;

        if (sortKey === "times_acquired") {
            valA = (a[1].times_won ?? 0) + (a[1].times_lost ?? 0);
            valB = (b[1].times_won ?? 0) + (b[1].times_lost ?? 0);
        } else {
            valA = a[1][sortKey] ?? 0;
            valB = b[1][sortKey] ?? 0;
        }

        return ascending ? valA - valB : valB - valA;
    });

    const handleSort = (key) => { // function to handle sort settings for any parameter
        if (sortKey === key) { 
            setAscending(!ascending);
        } else {
            setSortKey(key);
            setAscending(true);
        }
    };

    if (!relics) return <div>Loading...</div>;

    return (
        <div>
        <h2>Relics</h2>

        <table border="1" cellPadding="8">
            <thead>
            <tr>
                <th onClick={() => handleSort("id")}>Name</th>
                <th onClick={() => handleSort("winrate")}>Win Rate</th>
                <th onClick={() => handleSort("pickrate")}>Pick Rate</th>
                <th onClick={() => handleSort("times_acquired")}>Times Acquired</th>
            </tr>
            </thead>

            <tbody>
            {sorted.map(([id, relic]) => (
                <tr key={id}>
                <td>{id}</td>
                <td>{(relic.winrate * 100).toFixed(1)}%</td>
                <td>{(relic.pickrate * 100).toFixed(1)}%</td>
                <td>{(relic.times_won ?? 0) + (relic.times_lost ?? 0)}</td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    );
}

export default Relics;