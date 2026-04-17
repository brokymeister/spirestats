import React, { useState } from "react";

function Cards({ cards }) {
    const [sortKey, setSortKey] = useState("id");
    const [ascending, setAscending] = useState(false);
    const sorted = Object.entries(cards).sort((a, b) => { // sort the card data by specified parameter
        if (sortKey === "id") { // if sorting by name
            return ascending
                ? a[0].localeCompare(b[0])
                : b[0].localeCompare(a[0]);
        }

        const valA = a[1][sortKey] ?? 0;
        const valB = b[1][sortKey] ?? 0;

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

    if (!cards) return <div>Loading...</div>;

    return (
        <div>
        <h2>Cards</h2>

        <table border="1" cellPadding="8">
            <thead>
            <tr>
                <th onClick={() => handleSort("id")}>Name</th>
                <th onClick={() => handleSort("pickrate")}>Pick Rate</th>
                <th onClick={() => handleSort("winrate")}>Win Rate</th>
                <th onClick={() => handleSort("times_picked")}>Times Picked</th>
            </tr>
            </thead>

            <tbody>
            {sorted.map(([id, card]) => (
                <tr key={id}>
                <td>{id}</td>
                <td>{(card.pickrate * 100).toFixed(1)}%</td>
                <td>{(card.winrate * 100).toFixed(1)}%</td>
                <td>{card.times_picked}</td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    );
}

export default Cards;